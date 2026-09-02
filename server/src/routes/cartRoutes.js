const express = require('express');
const CartController = require('../controllers/cartController');
const { authenticate } = require('../middlewares/authMiddleware');

const router = express.Router();

router.use(authenticate);

router.get('/', CartController.getCart);
router.post('/items', CartController.addToCart);
router.put('/items/:cartItemId', CartController.updateQuantity);
router.delete('/items/:cartItemId', CartController.removeFromCart);

module.exports = router;
