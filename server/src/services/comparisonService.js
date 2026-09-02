const db = require('../database/db');

class ComparisonService {
  static compareProducts(productIds = []) {
    if (!productIds || productIds.length === 0) return [];

    const placeholders = productIds.map(() => '?').join(',');
    const products = db.prepare(`
      SELECT p.*, s.business_name as seller_name, c.name as category_name,
             (SELECT image_url FROM product_images WHERE product_id = p.id ORDER BY is_primary DESC LIMIT 1) as primary_image,
             COALESCE((SELECT AVG(rating) FROM reviews WHERE product_id = p.id AND status = 'APPROVED'), 0.0) as rating_avg,
             COALESCE((SELECT COUNT(*) FROM reviews WHERE product_id = p.id AND status = 'APPROVED'), 0) as review_count
      FROM products p
      JOIN sellers s ON p.seller_id = s.id
      JOIN categories c ON p.category_id = c.id
      WHERE p.id IN (${placeholders})
    `).all(...productIds);

    return products.map(product => {
      const specs = db.prepare('SELECT spec_key, spec_value FROM product_specifications WHERE product_id = ?').all(product.id);
      const variants = db.prepare(`
        SELECT v.variant_name, v.sku, i.quantity_on_hand
        FROM product_variants v
        JOIN inventory i ON v.id = i.variant_id
        WHERE v.product_id = ?
      `).all(product.id);

      const specMap = {};
      specs.forEach(s => { specMap[s.spec_key] = s.spec_value; });

      return {
        ...product,
        effective_price: parseFloat((product.base_price * (1 - product.discount_percent / 100)).toFixed(2)),
        specifications: specMap,
        variants
      };
    });
  }
}

module.exports = ComparisonService;
