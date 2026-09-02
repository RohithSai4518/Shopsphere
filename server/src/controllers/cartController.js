const CartService = require('../services/cartService');
const HTTP_STATUS = require('../constants/statusCodes');

class CartController {
  static getCart(req, res, next) {
    try {
      const cart = CartService.getCart(req.user.userId);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: cart,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static addToCart(req, res, next) {
    try {
      const { variantId, quantity } = req.body;
      const cart = CartService.addToCart(req.user.userId, variantId, quantity || 1);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: cart,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static updateQuantity(req, res, next) {
    try {
      const { cartItemId } = req.params;
      const { quantity } = req.body;
      const cart = CartService.updateQuantity(req.user.userId, cartItemId, quantity);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: cart,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static removeFromCart(req, res, next) {
    try {
      const { cartItemId } = req.params;
      const cart = CartService.removeFromCart(req.user.userId, cartItemId);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: cart,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = CartController;
