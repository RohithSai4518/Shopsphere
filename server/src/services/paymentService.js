const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class PaymentService {
  /**
   * Abstract Payment Gateway Interface
   * Processes mock payment without ever receiving or storing raw credit card details.
   */
  static processPayment({ orderId, amount, currency = 'USD', paymentMethodToken = 'mock_token_success' }) {
    if (!amount || amount <= 0) {
      throw new AppError('Payment amount must be greater than zero.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.VALIDATION_ERROR);
    }

    // Simulate Payment Provider Response
    const isSuccess = paymentMethodToken !== 'mock_token_fail';

    if (!isSuccess) {
      return {
        success: false,
        transactionRef: `tx_fail_${Date.now()}`,
        status: 'FAILED',
        errorReason: 'Payment method declined by issuing bank sandbox.'
      };
    }

    const transactionRef = `tx_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;

    return {
      success: true,
      provider: 'MOCK_PAYMENT_GATEWAY',
      transactionRef,
      amount: parseFloat(amount.toFixed(2)),
      currency,
      status: 'CAPTURED',
      processedAt: new Date().toISOString()
    };
  }

  static processRefund({ transactionRef, amount, reason }) {
    return {
      success: true,
      refundRef: `ref_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`,
      originalTransactionRef: transactionRef,
      amount: parseFloat(amount.toFixed(2)),
      status: 'REFUNDED',
      refundedAt: new Date().toISOString()
    };
  }
}

module.exports = PaymentService;
