const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class ReviewService {
  static createReview(userId, { productId, rating, title, comment }) {
    if (!rating || rating < 1 || rating > 5) {
      throw new AppError('Rating must be between 1 and 5 stars.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.VALIDATION_ERROR);
    }

    // Check if verified purchase
    const orderItem = db.prepare(`
      SELECT oi.id
      FROM order_items oi
      JOIN orders o ON oi.order_id = o.id
      JOIN product_variants v ON oi.variant_id = v.id
      WHERE o.user_id = ? AND v.product_id = ? AND o.status = 'DELIVERED'
    `).get(userId, productId);

    const reviewId = `rev_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    db.prepare(`
      INSERT OR REPLACE INTO reviews (id, product_id, user_id, rating, title, comment, is_verified_purchase, status)
      VALUES (?, ?, ?, ?, ?, ?, ?, 'APPROVED')
    `).run(reviewId, productId, userId, rating, title, comment, orderItem ? 1 : 0);

    return { reviewId, productId, rating, isVerified: !!orderItem };
  }

  static voteReview(userId, reviewId, voteType) {
    const validVote = ['HELPFUL', 'UNHELPFUL'].includes(voteType) ? voteType : 'HELPFUL';
    db.prepare('INSERT OR REPLACE INTO review_votes (review_id, user_id, vote_type) VALUES (?, ?, ?)').run(reviewId, userId, validVote);

    const counts = db.prepare(`
      SELECT
        SUM(CASE WHEN vote_type = 'HELPFUL' THEN 1 ELSE 0 END) as helpful,
        SUM(CASE WHEN vote_type = 'UNHELPFUL' THEN 1 ELSE 0 END) as unhelpful
      FROM review_votes WHERE review_id = ?
    `).get(reviewId);

    db.prepare('UPDATE reviews SET helpful_votes = ?, unhelpful_votes = ? WHERE id = ?').run(counts.helpful || 0, counts.unhelpful || 0, reviewId);
    return { reviewId, helpful: counts.helpful || 0, unhelpful: counts.unhelpful || 0 };
  }

  static addSellerResponse(sellerUserId, reviewId, responseText) {
    const seller = db.prepare('SELECT id FROM sellers WHERE user_id = ?').get(sellerUserId);
    if (!seller) throw new AppError('Seller account required.', HTTP_STATUS.FORBIDDEN, ERROR_CODES.FORBIDDEN);

    db.prepare('UPDATE reviews SET seller_response = ? WHERE id = ?').run(responseText, reviewId);
    return { reviewId, sellerResponse: responseText };
  }
}

module.exports = ReviewService;
