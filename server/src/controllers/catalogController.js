const CatalogService = require('../services/catalogService');
const HTTP_STATUS = require('../constants/statusCodes');

class CatalogController {
  static getCategories(req, res, next) {
    try {
      const tree = CatalogService.getCategoryTree();
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: tree,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static getProducts(req, res, next) {
    try {
      const result = CatalogService.getProducts(req.query);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: result.products,
        meta: {
          ...result.pagination,
          timestamp: new Date().toISOString()
        }
      });
    } catch (error) {
      next(error);
    }
  }

  static getProductById(req, res, next) {
    try {
      const result = CatalogService.getProductById(req.params.id);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: result,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static createProduct(req, res, next) {
    try {
      const result = CatalogService.createProduct(req.user.sellerId || req.user.userId, req.body);
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

module.exports = CatalogController;
