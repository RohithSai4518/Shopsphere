const WishlistService = require('../services/wishlistService');
const HTTP_STATUS = require('../constants/statusCodes');

class WishlistController {
  static getWishlists(req, res, next) {
    try {
      const wishlists = WishlistService.getWishlists(req.user.userId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: wishlists, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static createWishlist(req, res, next) {
    try {
      const wishlists = WishlistService.createWishlist(req.user.userId, req.body.name, req.body.isPublic);
      res.status(HTTP_STATUS.CREATED).json({ success: true, data: wishlists, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static addItem(req, res, next) {
    try {
      const wishlists = WishlistService.addItem(req.user.userId, req.params.wishlistId, req.body.productId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: wishlists, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static removeItem(req, res, next) {
    try {
      const wishlists = WishlistService.removeItem(req.user.userId, req.params.itemId);
      res.status(HTTP_STATUS.OK).json({ success: true, data: wishlists, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }

  static createPriceAlert(req, res, next) {
    try {
      const alert = WishlistService.createPriceAlert(req.user.userId, req.body.productId, req.body.targetPrice);
      res.status(HTTP_STATUS.CREATED).json({ success: true, data: alert, meta: { timestamp: new Date().toISOString() } });
    } catch (error) { next(error); }
  }
}

module.exports = WishlistController;
