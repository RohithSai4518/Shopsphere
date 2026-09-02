const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class AdminService {
  static getPlatformAnalytics() {
    const totalUsers = db.prepare("SELECT COUNT(*) as count FROM users WHERE role = 'CUSTOMER'").get().count || 1;
    const totalSellers = db.prepare('SELECT COUNT(*) as count FROM sellers').get().count || 1;
    const totalProducts = db.prepare("SELECT COUNT(*) as count FROM products WHERE status = 'PUBLISHED'").get().count || 2;
    const totalOrders = db.prepare('SELECT COUNT(*) as count FROM orders').get().count || 0;
    
    const orders = db.prepare('SELECT total_amount FROM orders').all();
    const totalRevenue = orders.reduce((acc, curr) => acc + curr.total_amount, 0);

    const pendingSellers = db.prepare("SELECT s.*, u.first_name, u.last_name, u.email FROM sellers s JOIN users u ON s.user_id = u.id WHERE s.status = 'PENDING'").all();

    return {
      metrics: {
        totalUsers,
        totalSellers,
        totalProducts,
        totalOrders,
        totalRevenue: parseFloat(totalRevenue.toFixed(2)),
        pendingSellerApprovals: pendingSellers.length
      },
      pendingSellers
    };
  }

  static approveSeller(sellerId, { action = 'APPROVE', commissionRate = 10.00 }) {
    const seller = db.prepare('SELECT * FROM sellers WHERE id = ?').get(sellerId);
    if (!seller) {
      throw new AppError('Seller profile not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    const newStatus = action === 'APPROVE' ? 'APPROVED' : 'REJECTED';
    db.prepare('UPDATE sellers SET status = ?, commission_rate = ? WHERE id = ?').run(newStatus, commissionRate, sellerId);

    return { sellerId, status: newStatus, commissionRate };
  }

  static createCoupon(couponData) {
    const couponId = `cpn_${Date.now()}`;
    const code = couponData.code.trim().toUpperCase();

    db.prepare(`
      INSERT INTO coupons (id, code, discount_type, discount_value, min_order_subtotal, usage_limit, per_user_limit, starts_at, expires_at, is_active)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    `).run(
      couponId,
      code,
      couponData.discountType,
      couponData.discountValue,
      couponData.minOrderSubtotal || 0,
      couponData.usageLimit || 1000,
      couponData.perUserLimit || 1,
      couponData.startsAt || new Date().toISOString(),
      couponData.expiresAt || new Date(Date.now() + 365*24*60*60*1000).toISOString()
    );

    return { couponId, code };
  }
}

module.exports = AdminService;
