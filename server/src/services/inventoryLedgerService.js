const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class InventoryLedgerService {
  static recordTransaction(variantId, type, quantity, referenceType, referenceId, notes = null) {
    const validTypes = ['RECEIPT', 'DEDUCTION', 'RESERVATION', 'RELEASE', 'ADJUSTMENT', 'RETURN'];
    if (!validTypes.includes(type)) {
      throw new AppError('Invalid inventory transaction type.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.VALIDATION_ERROR);
    }

    const inv = db.prepare('SELECT quantity_on_hand, quantity_reserved FROM inventory WHERE variant_id = ?').get(variantId);
    if (!inv) {
      db.prepare('INSERT INTO inventory (id, variant_id, quantity_on_hand) VALUES (?, ?, 0)').run(`inv_${Date.now()}`, variantId);
    }

    const txId = `inv_tx_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    db.prepare(`
      INSERT INTO inventory_transactions (id, variant_id, transaction_type, quantity, reference_type, reference_id, notes)
      VALUES (?, ?, ?, ?, ?, ?, ?)
    `).run(txId, variantId, type, quantity, referenceType, referenceId || null, notes);

    // Update aggregated inventory counters
    let newQty = inv ? inv.quantity_on_hand : 0;
    let newReserved = inv ? inv.quantity_reserved : 0;

    if (type === 'RECEIPT' || type === 'RETURN') newQty += quantity;
    if (type === 'DEDUCTION') newQty = Math.max(0, newQty - quantity);
    if (type === 'RESERVATION') newReserved += quantity;
    if (type === 'RELEASE') newReserved = Math.max(0, newReserved - quantity);

    db.prepare('UPDATE inventory SET quantity_on_hand = ?, quantity_reserved = ?, updated_at = datetime("now") WHERE variant_id = ?').run(newQty, newReserved, variantId);

    return { txId, variantId, newQuantityOnHand: newQty, newQuantityReserved: newReserved };
  }

  static getLedgerHistory(variantId) {
    return db.prepare('SELECT * FROM inventory_transactions WHERE variant_id = ? ORDER BY created_at DESC').all(variantId);
  }
}

module.exports = InventoryLedgerService;
