const db = require('../database/db');
const PaymentService = require('./paymentService');
const InventoryLedgerService = require('./inventoryLedgerService');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class ReturnsService {
  static createReturnRequest(userId, { orderId, orderItemId, reason, details }) {
    const item = db.prepare(`
      SELECT oi.*, o.user_id, o.status as order_status
      FROM order_items oi
      JOIN orders o ON oi.order_id = o.id
      WHERE oi.id = ? AND o.id = ? AND o.user_id = ?
    `).get(orderItemId, orderId, userId);

    if (!item) {
      throw new AppError('Order item not found or ineligible for return.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    const returnId = `ret_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    const refundAmount = item.total_price;

    db.prepare(`
      INSERT INTO return_requests (id, order_id, order_item_id, user_id, reason, details, status, refund_amount)
      VALUES (?, ?, ?, ?, ?, ?, 'REQUESTED', ?)
    `).run(returnId, orderId, orderItemId, userId, reason, details || null, refundAmount);

    return { returnId, status: 'REQUESTED', refundAmount };
  }

  static processReturnApproval(sellerOrAdminId, returnId, { action, sellerNotes }) {
    const ret = db.prepare('SELECT * FROM return_requests WHERE id = ?').get(returnId);
    if (!ret) throw new AppError('Return request not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);

    const newStatus = action === 'APPROVE' ? 'APPROVED' : 'REJECTED';
    db.prepare('UPDATE return_requests SET status = ?, seller_notes = ? WHERE id = ?').run(newStatus, sellerNotes || null, returnId);

    // If approved, initiate sandbox refund
    if (newStatus === 'APPROVED') {
      const payment = db.prepare('SELECT transaction_ref FROM payments WHERE order_id = ?').get(ret.order_id);
      if (payment) {
        PaymentService.processRefund({
          transactionRef: payment.transaction_ref,
          amount: ret.refund_amount,
          reason: ret.reason
        });
      }

      // Restock inventory via ledger
      const item = db.prepare('SELECT variant_id, quantity FROM order_items WHERE id = ?').get(ret.order_item_id);
      if (item) {
        InventoryLedgerService.recordTransaction(item.variant_id, 'RETURN', item.quantity, 'RETURN', returnId, 'Returned item restocked to inventory');
      }

      db.prepare("UPDATE return_requests SET status = 'REFUNDED' WHERE id = ?").run(returnId);
    }

    return { returnId, status: newStatus === 'APPROVED' ? 'REFUNDED' : 'REJECTED' };
  }

  static getUserReturns(userId) {
    return db.prepare('SELECT * FROM return_requests WHERE user_id = ? ORDER BY created_at DESC').all(userId);
  }
}

module.exports = ReturnsService;
