const express = require('express');
const WishlistController = require('../controllers/wishlistController');
const { authenticate } = require('../middlewares/authMiddleware');

const router = express.Router();
router.use(authenticate);

router.get('/', WishlistController.getWishlists);
router.post('/', WishlistController.createWishlist);
router.post('/:wishlistId/items', WishlistController.addItem);
router.delete('/items/:itemId', WishlistController.removeItem);
router.post('/price-alerts', WishlistController.createPriceAlert);

module.exports = router;
