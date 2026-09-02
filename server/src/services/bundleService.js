const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');

class BundleService {
  static getProductSpecifications(productId) {
    return db.prepare('SELECT * FROM product_specifications WHERE product_id = ? ORDER BY display_order ASC').all(productId);
  }

  static getActiveBundles() {
    const bundles = db.prepare('SELECT * FROM product_bundles WHERE is_active = 1 ORDER BY created_at DESC').all();
    return bundles.map(b => {
      const items = db.prepare(`
        SELECT bi.quantity, v.variant_name, v.sku, p.name as product_name, p.base_price,
               (SELECT image_url FROM product_images WHERE product_id = p.id ORDER BY is_primary DESC LIMIT 1) as primary_image
        FROM bundle_items bi
        JOIN product_variants v ON bi.variant_id = v.id
        JOIN products p ON v.product_id = p.id
        WHERE bi.bundle_id = ?
      `).all(b.id);
      return { ...b, items };
    });
  }

  static getRelatedProducts(productId, limit = 4) {
    const target = db.prepare('SELECT category_id, brand_id FROM products WHERE id = ?').get(productId);
    if (!target) return [];

    return db.prepare(`
      SELECT p.*,
             (SELECT image_url FROM product_images WHERE product_id = p.id ORDER BY is_primary DESC LIMIT 1) as primary_image
      FROM products p
      WHERE p.id != ? AND p.status = 'PUBLISHED' AND (p.category_id = ? OR p.brand_id = ?)
      ORDER BY p.created_at DESC
      LIMIT ?
    `).all(productId, target.category_id, target.brand_id || '', parseInt(limit));
  }
}

module.exports = BundleService;
