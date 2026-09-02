const express = require('express');
const CatalogController = require('../controllers/catalogController');
const { authenticate, authorize } = require('../middlewares/authMiddleware');

const router = express.Router();

router.get('/categories', CatalogController.getCategories);
router.get('/products', CatalogController.getProducts);
router.get('/products/:id', CatalogController.getProductById);

router.post('/products', authenticate, authorize('SELLER', 'ADMIN'), CatalogController.createProduct);

module.exports = router;
