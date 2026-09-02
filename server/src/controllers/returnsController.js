const ReturnsService = require('../services/returnsService');
const HTTP_STATUS = require('../constants/statusCodes');

class ReturnsController {
  static createReturnRequest(req, res, next) {
    try {
      const result = ReturnsService.createReturnRequest(req.user.userId, req.body);
      res.status(HTTP_STATUS.CREATED).json({ success: true, data: result, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getUserReturns(req, res, next) {
    try {
      const returns = ReturnsService.getUserReturns(req.user.userId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: returns, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static processReturnApproval(req, res, next) {
    try {
      const result = ReturnsService.processReturnApproval(req.user.userId, req.params.id, req.body);
      res.status(HTTP_STATUS.OK).json({ success: true, data: result, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }
}

module.exports = ReturnsController;
