const express = require('express');
const AdminController = require('../controllers/adminController');
const { authenticate, authorize } = require('../middlewares/authMiddleware');

const router = express.Router();

router.use(authenticate, authorize('ADMIN'));

router.get('/analytics', AdminController.getAnalytics);
router.post('/sellers/:id/approve', AdminController.approveSeller);
router.post('/coupons', AdminController.createCoupon);

module.exports = router;
