const express = require('express');
const RbacController = require('../controllers/rbacController');
const { authenticate, authorize } = require('../middlewares/authMiddleware');

const router = express.Router();
router.use(authenticate, authorize('ADMIN'));

router.get('/roles', RbacController.getRoles);
router.get('/permissions', RbacController.getPermissions);
router.post('/user-roles', RbacController.assignRole);

module.exports = router;
