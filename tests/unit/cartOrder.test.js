const assert = require('assert');
const test = require('node:test');

process.env.NODE_ENV = 'test';
process.env.DB_FILE = './data/test_cartOrder.json';

const AuthService = require('../../server/src/services/authService');
const CartService = require('../../server/src/services/cartService');
const CouponService = require('../../server/src/services/couponService');
const OrderService = require('../../server/src/services/orderService');
const { seedDatabase } = require('../../server/src/database/seed.js');

test('Cart & Order Service Integration Tests', async (t) => {
  seedDatabase();

  const userId = 'usr_customer_001';

  await t.test('1. Should fetch active cart items and correct subtotal summary', () => {
    const cart = CartService.getCart(userId);
    assert.ok(Array.isArray(cart.items));
    assert.strictEqual(typeof cart.summary.total, 'number');
  });

  await t.test('2. Should add product variant to cart and calculate summary', () => {
    CartService.addToCart(userId, 'var_laptop_01_32gb', 1);
    const cart = CartService.getCart(userId);
    const laptopItem = cart.items.find(i => i.variantId === 'var_laptop_01_32gb');
    assert.ok(laptopItem);
    assert.strictEqual(laptopItem.quantity, 1);
  });

  await t.test('3. Should validate promotional coupon WELCOME10', () => {
    const coupon = CouponService.validateCoupon('WELCOME10', userId, 500.00);
    assert.strictEqual(coupon.code, 'WELCOME10');
    assert.strictEqual(coupon.calculatedDiscount, 50.00);
  });

  await t.test('4. Should complete multi-step checkout order transaction', () => {
    CartService.clearCart(userId);
    CartService.addToCart(userId, 'var_laptop_01_32gb', 1);

    const shippingAddress = {
      fullName: 'Jane Shopper',
      streetAddress1: '100 Synthetic Way',
      city: 'Innovation City',
      state: 'CA',
      postalCode: '90210',
      country: 'United States'
    };

    const order = OrderService.createOrder(userId, {
      shippingAddress,
      couponCode: 'WELCOME10',
      paymentMethodToken: 'mock_token_success'
    });

    assert.strictEqual(order.status, 'CONFIRMED');
    assert.ok(order.orderNumber.startsWith('ORD-'));
    assert.strictEqual(order.discountAmount, 135.00);
  });
});
