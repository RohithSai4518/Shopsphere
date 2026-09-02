const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class CouponService {
  static validateCoupon(code, userId, subtotal) {
    if (!code) return null;

    const coupon = db.prepare('SELECT * FROM coupons WHERE code = ?').get(code.trim().toUpperCase());
    if (!coupon || !coupon.is_active) {
      throw new AppError('Invalid or inactive coupon code.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.COUPON_INVALID);
    }

    const now = new Date();
    if (new Date(coupon.starts_at) > now || new Date(coupon.expires_at) < now) {
      throw new AppError('Coupon code has expired.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.COUPON_INVALID);
    }

    if (subtotal < coupon.min_order_subtotal) {
      throw new AppError(
        `Order subtotal ($${subtotal.toFixed(2)}) does not meet the minimum requirement ($${coupon.min_order_subtotal.toFixed(2)}) for coupon ${coupon.code}.`,
        HTTP_STATUS.BAD_REQUEST,
        ERROR_CODES.COUPON_INVALID
      );
    }

    // Calculate discount
    let discount = 0;
    if (coupon.discount_type === 'PERCENTAGE') {
      discount = (subtotal * coupon.discount_value) / 100;
      if (coupon.max_discount_amount && discount > coupon.max_discount_amount) {
        discount = coupon.max_discount_amount;
      }
    } else if (coupon.discount_type === 'FIXED') {
      discount = coupon.discount_value;
    }

    discount = Math.min(discount, subtotal);

    return {
      couponId: coupon.id,
      code: coupon.code,
      discountType: coupon.discount_type,
      discountValue: coupon.discount_value,
      calculatedDiscount: parseFloat(discount.toFixed(2))
    };
  }
}

module.exports = CouponService;
