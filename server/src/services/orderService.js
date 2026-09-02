const db = require('../database/db');
const CartService = require('./cartService');
const CouponService = require('./couponService');
const PaymentService = require('./paymentService');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class OrderService {
  static createOrder(userId, { shippingAddress, billingAddress, couponCode, paymentMethodToken }) {
    const cart = CartService.getCart(userId);

    if (!cart.items || cart.items.length === 0) {
      throw new AppError('Your cart is empty. Add products before checking out.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.VALIDATION_ERROR);
    }

    // 1. Stock verification & transaction lock
    for (const item of cart.items) {
      if (item.quantity > item.stockAvailable) {
        throw new AppError(
          `Insufficient stock for "${item.productName} (${item.variantName})". Requested: ${item.quantity}, Available: ${item.stockAvailable}.`,
          HTTP_STATUS.BAD_REQUEST,
          ERROR_CODES.INSUFFICIENT_STOCK
        );
      }
    }

    // 2. Server-side Financial Calculations
    let subtotal = cart.summary.subtotal;
    let taxAmount = cart.summary.taxEstimate;
    let shippingAmount = cart.summary.shippingEstimate;
    let discountAmount = 0;
    let couponInfo = null;

    if (couponCode) {
      couponInfo = CouponService.validateCoupon(couponCode, userId, subtotal);
      if (couponInfo) {
        discountAmount = couponInfo.calculatedDiscount;
      }
    }

    const totalAmount = parseFloat(Math.max(0, subtotal - discountAmount + taxAmount + shippingAmount).toFixed(2));
    const orderId = `ord_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
    const orderNumber = `ORD-${new Date().toISOString().slice(0,10).replace(/-/g,'')}-${Math.floor(1000 + Math.random() * 9000)}`;

    return db.transaction(() => {
      // 3. Process Payment
      const paymentResult = PaymentService.processPayment({
        orderId,
        amount: totalAmount,
        paymentMethodToken
      });

      if (!paymentResult.success) {
        throw new AppError(paymentResult.errorReason || 'Payment authorization failed.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.PAYMENT_FAILED);
      }

      // 4. Create Order Record
      db.prepare(`
        INSERT INTO orders (
          id, order_number, user_id, status, subtotal, tax_amount,
          shipping_amount, discount_amount, total_amount, coupon_id,
          shipping_address_json, billing_address_json
        ) VALUES (?, ?, ?, 'CONFIRMED', ?, ?, ?, ?, ?, ?, ?, ?)
      `).run(
        orderId, orderNumber, userId, subtotal, taxAmount,
        shippingAmount, discountAmount, totalAmount, couponInfo ? couponInfo.couponId : null,
        JSON.stringify(shippingAddress), JSON.stringify(billingAddress || shippingAddress)
      );

      // 5. Create Order Items & Decrement Inventory
      for (const item of cart.items) {
        const orderItemId = `ori_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
        db.prepare(`
          INSERT INTO order_items (
            id, order_id, variant_id, seller_id, unit_price,
            discount_amount, tax_amount, quantity, total_price, item_status
          ) VALUES (?, ?, ?, ?, ?, 0.00, 0.00, ?, ?, 'PENDING')
        `).run(orderItemId, orderId, item.variantId, item.sellerId || 'sel_apex_001', item.unitPrice, item.quantity, item.itemSubtotal);

        // Decrement stock
        const newStock = Math.max(0, item.stockAvailable - item.quantity);
        db.prepare('UPDATE inventory SET quantity_on_hand = ? WHERE variant_id = ?').run(newStock, item.variantId);
      }

      // 6. Record Payment
      db.prepare(`
        INSERT INTO payments (id, order_id, provider, transaction_ref, amount, currency, status, payload_json)
        VALUES (?, ?, ?, ?, ?, 'USD', 'CAPTURED', ?)
      `).run(`pay_${Date.now()}`, orderId, paymentResult.provider, paymentResult.transactionRef, totalAmount, JSON.stringify(paymentResult));

      // 7. Clear Cart
      CartService.clearCart(userId);

      return {
        orderId,
        orderNumber,
        status: 'CONFIRMED',
        subtotal,
        discountAmount,
        taxAmount,
        shippingAmount,
        totalAmount,
        transactionRef: paymentResult.transactionRef,
        itemCount: cart.items.length
      };
    })();
  }

  static getUserOrders(userId) {
    const orders = db.prepare('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC').all(userId);
    return orders.map(order => {
      const items = db.prepare('SELECT * FROM order_items WHERE order_id = ?').all(order.id);
      return {
        ...order,
        shippingAddress: JSON.parse(order.shipping_address_json || '{}'),
        billingAddress: JSON.parse(order.billing_address_json || '{}'),
        items
      };
    });
  }

  static getOrderById(userId, orderId) {
    const order = db.prepare('SELECT * FROM orders WHERE (id = ? OR order_number = ?) AND user_id = ?').get(orderId, orderId, userId);
    if (!order) {
      throw new AppError('Order not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }
    const items = db.prepare('SELECT * FROM order_items WHERE order_id = ?').all(order.id);
    const payment = db.prepare('SELECT provider, transaction_ref, status, created_at FROM payments WHERE order_id = ?').get(order.id);

    return {
      ...order,
      shippingAddress: JSON.parse(order.shipping_address_json || '{}'),
      billingAddress: JSON.parse(order.billing_address_json || '{}'),
      items,
      payment
    };
  }
}

module.exports = OrderService;
