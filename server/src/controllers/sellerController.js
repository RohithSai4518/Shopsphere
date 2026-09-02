const SellerService = require('../services/sellerService');
const HTTP_STATUS = require('../constants/statusCodes');

class SellerController {
  static getDashboard(req, res, next) {
    try {
      const data = SellerService.getDashboardMetrics(req.user.userId);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static fulfillOrderItem(req, res, next) {
    try {
      const result = SellerService.fulfillOrderItem(req.user.userId, req.params.orderItemId, req.body);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: result,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = SellerController;
