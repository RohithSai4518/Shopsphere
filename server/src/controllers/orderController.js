const OrderService = require('../services/orderService');
const HTTP_STATUS = require('../constants/statusCodes');

class OrderController {
  static createOrder(req, res, next) {
    try {
      const order = OrderService.createOrder(req.user.userId, req.body);
      res.status(HTTP_STATUS.CREATED).json({
        success: true,
        data: order,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static getUserOrders(req, res, next) {
    try {
      const orders = OrderService.getUserOrders(req.user.userId);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: orders,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static getOrderById(req, res, next) {
    try {
      const order = OrderService.getOrderById(req.user.userId, req.params.id);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: order,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = OrderController;
