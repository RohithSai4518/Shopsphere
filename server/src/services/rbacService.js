const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class RbacService {
  static getRoles() {
    return db.prepare('SELECT * FROM roles ORDER BY name ASC').all();
  }

  static getPermissions() {
    return db.prepare('SELECT * FROM permissions ORDER BY module ASC, permission_key ASC').all();
  }

  static getUserPermissions(userId) {
    const user = db.prepare('SELECT role FROM users WHERE id = ?').get(userId);
    if (!user) return [];

    // Admin has full wildcard access
    if (user.role === 'ADMIN') {
      return ['*'];
    }

    const roles = db.prepare('SELECT role_id FROM user_roles WHERE user_id = ?').all(userId);
    const roleIds = roles.map(r => r.role_id);
    
    if (roleIds.length === 0) return [];

    const placeholders = roleIds.map(() => '?').join(',');
    const permissions = db.prepare(`
      SELECT DISTINCT p.permission_key
      FROM permissions p
      JOIN role_permissions rp ON p.id = rp.permission_id
      WHERE rp.role_id IN (${placeholders})
    `).all(...roleIds);

    return permissions.map(p => p.permission_key);
  }

  static checkPermission(userId, requiredPermission) {
    const user = db.prepare('SELECT role FROM users WHERE id = ?').get(userId);
    if (!user) return false;
    if (user.role === 'ADMIN') return true;

    const userPerms = this.getUserPermissions(userId);
    return userPerms.includes('*') || userPerms.includes(requiredPermission);
  }

  static assignRoleToUser(userId, roleId) {
    const user = db.prepare('SELECT id FROM users WHERE id = ?').get(userId);
    if (!user) throw new AppError('User not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);

    const role = db.prepare('SELECT id FROM roles WHERE id = ?').get(roleId);
    if (!role) throw new AppError('Role not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);

    db.prepare('INSERT OR REPLACE INTO user_roles (user_id, role_id) VALUES (?, ?)').run(userId, roleId);
    return { userId, roleId, assigned: true };
  }
}

function requirePermission(permissionKey) {
  return (req, res, next) => {
    if (!req.user || !req.user.userId) {
      return next(new AppError('Authentication required.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.UNAUTHORIZED));
    }

    const hasAccess = RbacService.checkPermission(req.user.userId, permissionKey);
    if (!hasAccess) {
      return next(new AppError(`Permission denied. Required permission: ${permissionKey}`, HTTP_STATUS.FORBIDDEN, ERROR_CODES.FORBIDDEN));
    }

    next();
  };
}

module.exports = {
  RbacService,
  requirePermission
};
