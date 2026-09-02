const AccountService = require('../services/accountService');
const HTTP_STATUS = require('../constants/statusCodes');

class AccountController {
  static updateProfile(req, res, next) {
    try {
      const user = AccountService.updateProfile(req.user.userId, req.body);
      res.status(HTTP_STATUS.OK).json({ success: true, data: user, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static changePassword(req, res, next) {
    try {
      const result = AccountService.changePassword(req.user.userId, req.body);
      res.status(HTTP_STATUS.OK).json({ success: true, data: result, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getAddresses(req, res, next) {
    try {
      const addresses = AccountService.getAddresses(req.user.userId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: addresses, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static addAddress(req, res, next) {
    try {
      const addresses = AccountService.addAddress(req.user.userId, req.body);
      res.status(HTTP_STATUS.CREATED).json({ success: true, data: addresses, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static deleteAddress(req, res, next) {
    try {
      const addresses = AccountService.deleteAddress(req.user.userId, req.params.id);
      res.status(HTTP_STATUS.OK).json({ success: true, data: addresses, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getSessions(req, res, next) {
    try {
      const sessions = AccountService.getUserSessions(req.user.userId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: sessions, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static revokeSession(req, res, next) {
    try {
      const sessions = AccountService.revokeSession(req.user.userId, req.params.id);
      res.status(HTTP_STATUS.OK).json({ success: true, data: sessions, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getPreferences(req, res, next) {
    try {
      const prefs = AccountService.getPreferences(req.user.userId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: prefs, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static updatePreferences(req, res, next) {
    try {
      const prefs = AccountService.updatePreferences(req.user.userId, req.body);
      res.status(HTTP_STATUS.OK).json({ success: true, data: prefs, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getRecentlyViewed(req, res, next) {
    try {
      const items = AccountService.getRecentlyViewed(req.user.userId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: items, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }
}

module.exports = AccountController;
