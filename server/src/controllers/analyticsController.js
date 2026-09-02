const AuditService = require('../services/auditService');
const HTTP_STATUS = require('../constants/statusCodes');

class AnalyticsController {
  static getAuditLogs(req, res, next) {
    try {
      const logs = AuditService.getAuditLogs(req.query.page || 1, req.query.limit || 20);
      res.status(HTTP_STATUS.OK).json({ success: true, data: logs.logs, meta: { page: logs.page, limit: logs.limit, total: logs.total, timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }
}

module.exports = AnalyticsController;
