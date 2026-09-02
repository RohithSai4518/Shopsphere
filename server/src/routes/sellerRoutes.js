const express = require('express');
const SellerController = require('../controllers/sellerController');
const { authenticate, authorize } = require('../middlewares/authMiddleware');

const router = express.Router();

router.use(authenticate, authorize('SELLER', 'ADMIN'));

router.get('/dashboard', SellerController.getDashboard);
router.post('/orders/:orderItemId/fulfill', SellerController.fulfillOrderItem);

module.exports = router;
