const AdminService = require('../services/adminService');
const HTTP_STATUS = require('../constants/statusCodes');

class AdminController {
  static getAnalytics(req, res, next) {
    try {
      const data = AdminService.getPlatformAnalytics();
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static approveSeller(req, res, next) {
    try {
      const result = AdminService.approveSeller(req.params.id, req.body);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: result,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static createCoupon(req, res, next) {
    try {
      const result = AdminService.createCoupon(req.body);
      res.status(HTTP_STATUS.CREATED).json({
        success: true,
        data: result,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = AdminController;
