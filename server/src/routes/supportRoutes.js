const express = require('express');
const SupportController = require('../controllers/supportController');
const { authenticate, authorize } = require('../middlewares/authMiddleware');

const router = express.Router();
router.use(authenticate);

router.post('/tickets', SupportController.createTicket);
router.get('/tickets', SupportController.getUserTickets);
router.get('/tickets/admin/all', authorize('ADMIN', 'SUPPORT'), SupportController.getAllTicketsAdmin);
router.get('/tickets/:id', SupportController.getTicketDetails);
router.post('/tickets/:id/messages', SupportController.addMessage);

module.exports = router;
