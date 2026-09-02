const db = require('../database/db');
const bcrypt = require('bcryptjs');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class AccountService {
  static updateProfile(userId, { firstName, lastName, phone }) {
    const user = db.prepare('SELECT id FROM users WHERE id = ?').get(userId);
    if (!user) throw new AppError('User account not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);

    db.prepare(`
      UPDATE users
      SET first_name = ?, last_name = ?, phone = ?, updated_at = datetime('now')
      WHERE id = ?
    `).run(firstName, lastName, phone || null, userId);

    return db.prepare('SELECT id, email, first_name, last_name, phone, role FROM users WHERE id = ?').get(userId);
  }

  static changePassword(userId, { currentPassword, newPassword }) {
    const user = db.prepare('SELECT id, password_hash FROM users WHERE id = ?').get(userId);
    if (!user) throw new AppError('User account not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);

    const isMatch = bcrypt.compareSync(currentPassword, user.password_hash);
    if (!isMatch) {
      throw new AppError('Current password is incorrect.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.INVALID_CREDENTIALS);
    }

    if (!newPassword || newPassword.length < 8) {
      throw new AppError('New password must be at least 8 characters long.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.VALIDATION_ERROR);
    }

    const newHash = bcrypt.hashSync(newPassword, 12);
    db.prepare('UPDATE users SET password_hash = ?, updated_at = datetime("now") WHERE id = ?').run(newHash, userId);
    return { success: true, message: 'Password updated successfully.' };
  }

  static getAddresses(userId) {
    return db.prepare('SELECT * FROM addresses WHERE user_id = ? ORDER BY is_default DESC, created_at DESC').all(userId);
  }

  static addAddress(userId, addressData) {
    const addressId = `addr_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    
    if (addressData.isDefault) {
      db.prepare('UPDATE addresses SET is_default = 0 WHERE user_id = ?').run(userId);
    }

    db.prepare(`
      INSERT INTO addresses (id, user_id, address_type, full_name, street_address_1, street_address_2, city, state, postal_code, country, is_default)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      addressId, userId, addressData.addressType || 'SHIPPING', addressData.fullName,
      addressData.streetAddress1, addressData.streetAddress2 || null, addressData.city,
      addressData.state, addressData.postalCode, addressData.country, addressData.isDefault ? 1 : 0
    );

    return this.getAddresses(userId);
  }

  static deleteAddress(userId, addressId) {
    db.prepare('DELETE FROM addresses WHERE id = ? AND user_id = ?').run(addressId, userId);
    return this.getAddresses(userId);
  }

  static getUserSessions(userId) {
    return db.prepare('SELECT id, ip_address, user_agent, is_revoked, expires_at, created_at FROM user_sessions WHERE user_id = ? ORDER BY created_at DESC').all(userId);
  }

  static revokeSession(userId, sessionId) {
    db.prepare('UPDATE user_sessions SET is_revoked = 1 WHERE id = ? AND user_id = ?').run(sessionId, userId);
    return this.getUserSessions(userId);
  }

  static getPreferences(userId) {
    let prefs = db.prepare('SELECT * FROM user_preferences WHERE user_id = ?').get(userId);
    if (!prefs) {
      db.prepare("INSERT OR IGNORE INTO user_preferences (user_id) VALUES (?)").run(userId);
      prefs = db.prepare('SELECT * FROM user_preferences WHERE user_id = ?').get(userId);
    }
    return prefs;
  }

  static updatePreferences(userId, prefsData) {
    db.prepare(`
      INSERT OR REPLACE INTO user_preferences (user_id, email_notifications, sms_notifications, promotional_emails, theme, currency)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(
      userId,
      prefsData.emailNotifications ? 1 : 0,
      prefsData.smsNotifications ? 1 : 0,
      prefsData.promotionalEmails ? 1 : 0,
      prefsData.theme || 'DARK',
      prefsData.currency || 'USD'
    );
    return this.getPreferences(userId);
  }

  static recordRecentlyViewed(userId, productId) {
    db.prepare(`
      INSERT OR REPLACE INTO recently_viewed (user_id, product_id, viewed_at)
      VALUES (?, ?, datetime('now'))
    `).run(userId, productId);
  }

  static getRecentlyViewed(userId) {
    return db.prepare(`
      SELECT p.*, rv.viewed_at,
             (SELECT image_url FROM product_images WHERE product_id = p.id ORDER BY is_primary DESC LIMIT 1) as primary_image
      FROM recently_viewed rv
      JOIN products p ON rv.product_id = p.id
      WHERE rv.user_id = ?
      ORDER BY rv.viewed_at DESC
      LIMIT 10
    `).all(userId);
  }
}

module.exports = AccountService;
