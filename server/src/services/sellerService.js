const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class SellerService {
  static getDashboardMetrics(userId) {
    const seller = db.prepare('SELECT * FROM sellers WHERE user_id = ?').get(userId);
    if (!seller) {
      throw new AppError('Seller profile not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    const products = db.prepare('SELECT id, name, status FROM products WHERE seller_id = ?').all(seller.id);
    const orderItems = db.prepare('SELECT * FROM order_items WHERE seller_id = ?').all(seller.id);

    const totalRevenue = orderItems.reduce((acc, curr) => acc + curr.total_price, 0);
    const pendingFulfillments = orderItems.filter(i => i.item_status === 'PENDING').length;

    return {
      sellerProfile: seller,
      metrics: {
        totalProducts: products.length,
        totalOrders: orderItems.length,
        totalRevenue: parseFloat(totalRevenue.toFixed(2)),
        pendingFulfillments,
        ratingAverage: seller.rating_avg
      },
      recentItems: orderItems.slice(0, 10)
    };
  }

  static fulfillOrderItem(userId, orderItemId, { trackingNumber, carrier = 'Express Logistics' }) {
    const seller = db.prepare('SELECT id FROM sellers WHERE user_id = ?').get(userId);
    if (!seller) {
      throw new AppError('Seller profile not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    const item = db.prepare('SELECT * FROM order_items WHERE id = ? AND seller_id = ?').get(orderItemId, seller.id);
    if (!item) {
      throw new AppError('Order item not found or unauthorized.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    db.prepare("UPDATE order_items SET item_status = 'SHIPPED' WHERE id = ?").run(orderItemId);

    // Create shipment tracking record
    const shipmentId = `shp_${Date.now()}`;
    db.prepare(`
      INSERT INTO shipments (id, order_id, seller_id, carrier, tracking_number, status, shipped_at)
      VALUES (?, ?, ?, ?, ?, 'IN_TRANSIT', datetime('now'))
    `).run(shipmentId, item.order_id, seller.id, carrier, trackingNumber || `TRK-${Date.now()}`);

    return { shipmentId, trackingNumber, status: 'SHIPPED' };
  }
}

module.exports = SellerService;
