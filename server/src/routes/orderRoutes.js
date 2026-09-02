const express = require('express');
const OrderController = require('../controllers/orderController');
const { authenticate } = require('../middlewares/authMiddleware');

const router = express.Router();

router.use(authenticate);

router.post('/', OrderController.createOrder);
router.get('/', OrderController.getUserOrders);
router.get('/:id', OrderController.getOrderById);

module.exports = router;
