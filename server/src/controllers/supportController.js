const SupportService = require('../services/supportService');
const HTTP_STATUS = require('../constants/statusCodes');

class SupportController {
  static createTicket(req, res, next) {
    try {
      const ticket = SupportService.createTicket(req.user.userId, req.body);
      res.status(HTTP_STATUS.CREATED).json({ success: true, data: ticket, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getUserTickets(req, res, next) {
    try {
      const tickets = SupportService.getUserTickets(req.user.userId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: tickets, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getTicketDetails(req, res, next) {
    try {
      const details = SupportService.getTicketDetails(req.user.userId, req.params.id);
      res.status(HTTP_STATUS.OK).json({ success: true, data: details, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static addMessage(req, res, next) {
    try {
      const msg = SupportService.addMessage(req.user.userId, req.params.id, req.body.messageText, req.body.isInternalNote);
      res.status(HTTP_STATUS.CREATED).json({ success: true, data: msg, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static getAllTicketsAdmin(req, res, next) {
    try {
      const tickets = SupportService.getAllTicketsAdmin();
      res.status(HTTP_STATUS.OK).json({ success: true, data: tickets, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }
}

module.exports = SupportController;
