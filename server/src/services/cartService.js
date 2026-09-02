const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class CartService {
  static getCart(userId) {
    const items = db.prepare(`
      SELECT ci.id as cart_item_id, ci.quantity, ci.variant_id,
             v.sku, v.variant_name, v.price_override, v.attributes_json,
             p.id as product_id, p.name as product_name, p.base_price, p.discount_percent, p.tax_rate,
             s.id as seller_id, s.business_name as seller_name,
             i.quantity_on_hand,
             (SELECT image_url FROM product_images WHERE product_id = p.id ORDER BY is_primary DESC, display_order ASC LIMIT 1) as primary_image
      FROM cart_items ci
      JOIN product_variants v ON ci.variant_id = v.id
      JOIN products p ON v.product_id = p.id
      JOIN sellers s ON p.seller_id = s.id
      JOIN inventory i ON v.id = i.variant_id
      WHERE ci.user_id = ?
      ORDER BY ci.created_at DESC
    `).all(userId);

    let subtotal = 0;
    let totalTax = 0;

    const formattedItems = items.map(item => {
      const unitPrice = (typeof item.price_override === 'number' && !isNaN(item.price_override)) ? item.price_override : item.base_price;
      const effectiveUnitPrice = parseFloat((unitPrice * (1 - item.discount_percent / 100)).toFixed(2));
      const itemSubtotal = parseFloat((effectiveUnitPrice * item.quantity).toFixed(2));
      const itemTax = parseFloat((itemSubtotal * (item.tax_rate / 100)).toFixed(2));

      subtotal += itemSubtotal;
      totalTax += itemTax;

      return {
        cartItemId: item.cart_item_id,
        productId: item.product_id,
        variantId: item.variant_id,
        sku: item.sku,
        productName: item.product_name,
        variantName: item.variant_name,
        sellerName: item.seller_name,
        primaryImage: item.primary_image,
        unitPrice: effectiveUnitPrice,
        originalUnitPrice: unitPrice,
        discountPercent: item.discount_percent,
        quantity: item.quantity,
        stockAvailable: item.quantity_on_hand,
        itemSubtotal,
        attributes: JSON.parse(item.attributes_json || '{}')
      };
    });

    const shippingEstimate = subtotal > 100 || items.length === 0 ? 0.00 : 9.99;
    const total = parseFloat((subtotal + totalTax + shippingEstimate).toFixed(2));

    return {
      items: formattedItems,
      summary: {
        itemCount: items.reduce((acc, curr) => acc + curr.quantity, 0),
        subtotal: parseFloat(subtotal.toFixed(2)),
        taxEstimate: parseFloat(totalTax.toFixed(2)),
        shippingEstimate,
        total
      }
    };
  }

  static addToCart(userId, variantId, quantity = 1) {
    if (quantity <= 0) {
      throw new AppError('Quantity must be greater than zero.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.VALIDATION_ERROR);
    }

    // Check variant & stock
    const variant = db.prepare(`
      SELECT v.id, i.quantity_on_hand
      FROM product_variants v
      JOIN inventory i ON v.id = i.variant_id
      WHERE v.id = ?
    `).get(variantId);

    if (!variant) {
      throw new AppError('Product variant not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    // Check existing item in cart
    const existing = db.prepare('SELECT id, quantity FROM cart_items WHERE user_id = ? AND variant_id = ?').get(userId, variantId);
    const newQuantity = (existing ? existing.quantity : 0) + quantity;

    if (newQuantity > variant.quantity_on_hand) {
      throw new AppError(
        `Cannot add item to cart. Requested quantity (${newQuantity}) exceeds available stock (${variant.quantity_on_hand}).`,
        HTTP_STATUS.BAD_REQUEST,
        ERROR_CODES.INSUFFICIENT_STOCK
      );
    }

    if (existing) {
      db.prepare('UPDATE cart_items SET quantity = ?, updated_at = datetime("now") WHERE id = ?').run(newQuantity, existing.id);
    } else {
      const cartItemId = `crt_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
      db.prepare('INSERT INTO cart_items (id, user_id, variant_id, quantity) VALUES (?, ?, ?, ?)').run(cartItemId, userId, variantId, newQuantity);
    }

    return this.getCart(userId);
  }

  static updateQuantity(userId, cartItemId, quantity) {
    const item = db.prepare(`
      SELECT ci.id, ci.variant_id, i.quantity_on_hand
      FROM cart_items ci
      JOIN inventory i ON ci.variant_id = i.variant_id
      WHERE ci.id = ? AND ci.user_id = ?
    `).get(cartItemId, userId);

    if (!item) {
      throw new AppError('Cart item not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    if (quantity <= 0) {
      db.prepare('DELETE FROM cart_items WHERE id = ?').run(cartItemId);
    } else {
      if (quantity > item.quantity_on_hand) {
        throw new AppError(
          `Requested quantity (${quantity}) exceeds available stock (${item.quantity_on_hand}).`,
          HTTP_STATUS.BAD_REQUEST,
          ERROR_CODES.INSUFFICIENT_STOCK
        );
      }
      db.prepare('UPDATE cart_items SET quantity = ?, updated_at = datetime("now") WHERE id = ?').run(quantity, cartItemId);
    }

    return this.getCart(userId);
  }

  static removeFromCart(userId, cartItemId) {
    db.prepare('DELETE FROM cart_items WHERE id = ? AND user_id = ?').run(cartItemId, userId);
    return this.getCart(userId);
  }

  static clearCart(userId) {
    db.prepare('DELETE FROM cart_items WHERE user_id = ?').run(userId);
  }
}

module.exports = CartService;
