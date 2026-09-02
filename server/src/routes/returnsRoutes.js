const express = require('express');
const ReturnsController = require('../controllers/returnsController');
const { authenticate, authorize } = require('../middlewares/authMiddleware');

const router = express.Router();
router.use(authenticate);

router.post('/', ReturnsController.createReturnRequest);
router.get('/', ReturnsController.getUserReturns);
router.post('/:id/approve', authorize('SELLER', 'ADMIN'), ReturnsController.processReturnApproval);

module.exports = router;
