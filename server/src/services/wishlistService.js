const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class WishlistService {
  static getWishlists(userId) {
    let wishlists = db.prepare('SELECT * FROM wishlists WHERE user_id = ? ORDER BY created_at DESC').all(userId);
    if (wishlists.length === 0) {
      const defaultId = `wsh_${Date.now()}`;
      db.prepare("INSERT INTO wishlists (id, user_id, name, is_public) VALUES (?, ?, 'My Default Wishlist', 0)").run(defaultId, userId);
      wishlists = db.prepare('SELECT * FROM wishlists WHERE user_id = ?').all(userId);
    }

    return wishlists.map(w => {
      const items = db.prepare(`
        SELECT wi.id as wishlist_item_id, wi.created_at as added_at,
               p.id as product_id, p.name, p.base_price, p.discount_percent,
               (SELECT image_url FROM product_images WHERE product_id = p.id ORDER BY is_primary DESC LIMIT 1) as primary_image
        FROM wishlist_items wi
        JOIN products p ON wi.product_id = p.id
        WHERE wi.wishlist_id = ?
      `).all(w.id);
      return { ...w, items };
    });
  }

  static createWishlist(userId, name, isPublic = false) {
    const wishlistId = `wsh_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    db.prepare('INSERT INTO wishlists (id, user_id, name, is_public) VALUES (?, ?, ?, ?)').run(wishlistId, userId, name, isPublic ? 1 : 0);
    return this.getWishlists(userId);
  }

  static addItem(userId, wishlistId, productId) {
    const wishlist = db.prepare('SELECT id FROM wishlists WHERE id = ? AND user_id = ?').get(wishlistId, userId);
    if (!wishlist) throw new AppError('Wishlist not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);

    const itemId = `wshi_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    db.prepare('INSERT OR IGNORE INTO wishlist_items (id, wishlist_id, product_id) VALUES (?, ?, ?)').run(itemId, wishlistId, productId);
    return this.getWishlists(userId);
  }

  static removeItem(userId, wishlistItemId) {
    db.prepare(`
      DELETE FROM wishlist_items
      WHERE id = ? AND wishlist_id IN (SELECT id FROM wishlists WHERE user_id = ?)
    `).run(wishlistItemId, userId);
    return this.getWishlists(userId);
  }

  static createPriceAlert(userId, productId, targetPrice) {
    const alertId = `pal_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    db.prepare('INSERT OR REPLACE INTO price_alerts (id, user_id, product_id, target_price) VALUES (?, ?, ?, ?)').run(alertId, userId, productId, targetPrice);
    return { alertId, productId, targetPrice };
  }
}

module.exports = WishlistService;
