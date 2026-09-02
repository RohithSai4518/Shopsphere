const express = require('express');
const AnalyticsController = require('../controllers/analyticsController');
const { authenticate, authorize } = require('../middlewares/authMiddleware');

const router = express.Router();
router.use(authenticate, authorize('ADMIN'));

router.get('/audit-logs', AnalyticsController.getAuditLogs);

module.exports = router;
