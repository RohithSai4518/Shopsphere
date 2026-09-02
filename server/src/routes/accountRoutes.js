const express = require('express');
const AccountController = require('../controllers/accountController');
const { authenticate } = require('../middlewares/authMiddleware');

const router = express.Router();
router.use(authenticate);

router.put('/profile', AccountController.updateProfile);
router.put('/password', AccountController.changePassword);
router.get('/addresses', AccountController.getAddresses);
router.post('/addresses', AccountController.addAddress);
router.delete('/addresses/:id', AccountController.deleteAddress);
router.get('/sessions', AccountController.getSessions);
router.delete('/sessions/:id', AccountController.revokeSession);
router.get('/preferences', AccountController.getPreferences);
router.put('/preferences', AccountController.updatePreferences);
router.get('/recently-viewed', AccountController.getRecentlyViewed);

module.exports = router;
