const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class CatalogService {
  static getCategoryTree() {
    const categories = db.prepare('SELECT * FROM categories WHERE is_active = 1 ORDER BY display_order ASC, name ASC').all();
    const map = {};
    const tree = [];

    categories.forEach(cat => {
      map[cat.id] = { ...cat, children: [] };
    });

    categories.forEach(cat => {
      if (cat.parent_id && map[cat.parent_id]) {
        map[cat.parent_id].children.push(map[cat.id]);
      } else {
        tree.push(map[cat.id]);
      }
    });

    return tree;
  }

  static getProducts({
    keyword,
    categoryId,
    brand,
    minPrice,
    maxPrice,
    minRating,
    inStock,
    sortBy = 'newest',
    page = 1,
    limit = 20
  }) {
    let baseSql = `
      SELECT p.*, s.business_name as seller_name, c.name as category_name,
             (SELECT image_url FROM product_images WHERE product_id = p.id ORDER BY is_primary DESC, display_order ASC LIMIT 1) as primary_image,
             COALESCE((SELECT AVG(rating) FROM reviews WHERE product_id = p.id AND status = 'APPROVED'), 0.0) as rating_avg,
             COALESCE((SELECT COUNT(*) FROM reviews WHERE product_id = p.id AND status = 'APPROVED'), 0) as review_count
      FROM products p
      JOIN sellers s ON p.seller_id = s.id
      JOIN categories c ON p.category_id = c.id
      WHERE p.status = 'PUBLISHED'
    `;
    const params = [];

    if (keyword) {
      baseSql += ` AND (p.name LIKE ? OR p.description LIKE ? OR p.brand LIKE ?)`;
      const term = `%${keyword.trim()}%`;
      params.push(term, term, term);
    }

    if (categoryId) {
      baseSql += ` AND p.category_id = ?`;
      params.push(categoryId);
    }

    if (brand) {
      baseSql += ` AND LOWER(p.brand) = LOWER(?)`;
      params.push(brand);
    }

    if (minPrice) {
      baseSql += ` AND (p.base_price * (1 - p.discount_percent / 100)) >= ?`;
      params.push(parseFloat(minPrice));
    }

    if (maxPrice) {
      baseSql += ` AND (p.base_price * (1 - p.discount_percent / 100)) <= ?`;
      params.push(parseFloat(maxPrice));
    }

    // Sort order mapping
    let orderSql = ' ORDER BY p.created_at DESC';
    if (sortBy === 'price_low') orderSql = ' ORDER BY (p.base_price * (1 - p.discount_percent / 100)) ASC';
    if (sortBy === 'price_high') orderSql = ' ORDER BY (p.base_price * (1 - p.discount_percent / 100)) DESC';
    if (sortBy === 'rating') orderSql = ' ORDER BY rating_avg DESC';
    if (sortBy === 'popular') orderSql = ' ORDER BY review_count DESC';

    const offset = (page - 1) * limit;

    // Execute count query
    const countSql = `SELECT COUNT(*) as total FROM (${baseSql})`;
    const totalRow = db.prepare(countSql).get(...params);
    const total = totalRow ? totalRow.total : 0;

    // Execute paginated products query
    const paginatedSql = baseSql + orderSql + ` LIMIT ? OFFSET ?`;
    const products = db.prepare(paginatedSql).all(...params, parseInt(limit), parseInt(offset));

    return {
      products: products.map(p => ({
        ...p,
        effective_price: parseFloat((p.base_price * (1 - p.discount_percent / 100)).toFixed(2))
      })),
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total,
        totalPages: Math.ceil(total / limit)
      }
    };
  }

  static getProductById(productId) {
    const product = db.prepare(`
      SELECT p.*, s.business_name as seller_name, s.rating_avg as seller_rating, c.name as category_name
      FROM products p
      JOIN sellers s ON p.seller_id = s.id
      JOIN categories c ON p.category_id = c.id
      WHERE p.id = ? OR p.slug = ?
    `).get(productId, productId);

    if (!product) {
      throw new AppError('Product not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    const variants = db.prepare(`
      SELECT v.*, i.quantity_on_hand, i.quantity_reserved
      FROM product_variants v
      LEFT JOIN inventory i ON v.id = i.variant_id
      WHERE v.product_id = ?
    `).all(product.id);

    const images = db.prepare('SELECT * FROM product_images WHERE product_id = ? ORDER BY is_primary DESC, display_order ASC').all(product.id);

    const reviews = db.prepare(`
      SELECT r.*, u.first_name, u.last_name
      FROM reviews r
      JOIN users u ON r.user_id = u.id
      WHERE r.product_id = ? AND r.status = 'APPROVED'
      ORDER BY r.created_at DESC
      LIMIT 10
    `).all(product.id);

    const ratingStats = db.prepare(`
      SELECT AVG(rating) as avg_rating, COUNT(*) as review_count
      FROM reviews
      WHERE product_id = ? AND status = 'APPROVED'
    `).get(product.id);

    return {
      product: {
        ...product,
        effective_price: parseFloat((product.base_price * (1 - product.discount_percent / 100)).toFixed(2)),
        rating_avg: ratingStats.avg_rating || 0,
        review_count: ratingStats.review_count || 0
      },
      variants,
      images,
      reviews
    };
  }

  static createProduct(sellerId, data) {
    const productId = `prd_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
    const slug = data.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)+/g, '') + `-${Date.now().toString(36)}`;

    return db.transaction(() => {
      db.prepare(`
        INSERT INTO products (id, seller_id, category_id, name, slug, brand, description, base_price, discount_percent, tax_rate, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PUBLISHED')
      `).run(productId, sellerId, data.categoryId, data.name, slug, data.brand || null, data.description, data.basePrice, data.discountPercent || 0, data.taxRate || 0);

      // Create default variant
      const variantId = `var_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
      const sku = `SKU-${Date.now().toString(36).toUpperCase()}`;
      db.prepare(`
        INSERT INTO product_variants (id, product_id, sku, variant_name, price_override, attributes_json, is_default)
        VALUES (?, ?, ?, ?, ?, ?, 1)
      `).run(variantId, productId, sku, 'Standard', data.basePrice, JSON.stringify(data.attributes || {}));

      // Initialize inventory
      db.prepare(`
        INSERT INTO inventory (id, variant_id, quantity_on_hand, quantity_reserved)
        VALUES (?, ?, ?, 0)
      `).run(`inv_${Date.now()}`, variantId, data.stockQuantity || 50);

      // Add image
      if (data.imageUrl) {
        db.prepare(`
          INSERT INTO product_images (id, product_id, image_url, alt_text, display_order, is_primary)
          VALUES (?, ?, ?, ?, 1, 1)
        `).run(`img_${Date.now()}`, productId, data.imageUrl, data.name);
      }

      return { productId, slug };
    })();
  }
}

module.exports = CatalogService;
