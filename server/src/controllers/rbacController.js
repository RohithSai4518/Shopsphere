const { RbacService } = require('../services/rbacService');
const HTTP_STATUS = require('../constants/statusCodes');

class RbacController {
  static getRoles(req, res, next) {
    try {
      const roles = RbacService.getRoles();
      res.status(HTTP_STATUS.OK).json({ success: true, data: roles, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getPermissions(req, res, next) {
    try {
      const permissions = RbacService.getPermissions();
      res.status(HTTP_STATUS.OK).json({ success: true, data: permissions, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static assignRole(req, res, next) {
    try {
      const result = RbacService.assignRoleToUser(req.body.userId, req.body.roleId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: result, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }
}

module.exports = RbacController;
