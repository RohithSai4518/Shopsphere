const db = require('../database/db');
const bcrypt = require('bcryptjs');
const { v4: uuidv4 } = require('crypto');
const { generateAccessToken, generateRefreshToken, verifyRefreshToken } = require('../utils/token');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class AuthService {
  static registerUser({ email, password, firstName, lastName, phone, role = 'CUSTOMER', businessName = null }) {
    const existing = db.prepare('SELECT id FROM users WHERE email = ?').get(email.toLowerCase());
    if (existing) {
      throw new AppError('An account with this email address already exists.', HTTP_STATUS.CONFLICT, ERROR_CODES.RESOURCE_EXISTS);
    }

    const userId = `usr_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
    const passwordHash = bcrypt.hashSync(password, 12);
    const validRole = ['CUSTOMER', 'SELLER'].includes(role) ? role : 'CUSTOMER';

    return db.transaction(() => {
      // 1. Insert User
      db.prepare(`
        INSERT INTO users (id, email, password_hash, first_name, last_name, phone, role, is_verified, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'ACTIVE')
      `).run(userId, email.toLowerCase(), passwordHash, firstName, lastName, phone || null, validRole);

      // 2. If registering as SELLER, create pending seller profile
      let sellerProfile = null;
      if (validRole === 'SELLER') {
        const sellerId = `sel_${Date.now()}_${Math.random().toString(36).substr(2, 5)}`;
        db.prepare(`
          INSERT INTO sellers (id, user_id, business_name, business_email, business_phone, status, commission_rate)
          VALUES (?, ?, ?, ?, ?, 'PENDING', 10.00)
        `).run(sellerId, userId, businessName || `${firstName}'s Store`, email.toLowerCase(), phone || null);
        sellerProfile = { sellerId, status: 'PENDING', businessName };
      }

      const payload = { userId, email: email.toLowerCase(), role: validRole };
      const accessToken = generateAccessToken(payload);
      const refreshToken = generateRefreshToken(payload);

      return {
        user: { id: userId, email: email.toLowerCase(), firstName, lastName, role: validRole, sellerProfile },
        accessToken,
        refreshToken
      };
    })();
  }

  static loginUser({ email, password }) {
    const user = db.prepare('SELECT * FROM users WHERE email = ?').get(email.toLowerCase());
    if (!user) {
      throw new AppError('Invalid email or password.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.INVALID_CREDENTIALS);
    }

    if (user.status !== 'ACTIVE') {
      throw new AppError('Your account has been suspended or deactivated.', HTTP_STATUS.FORBIDDEN, ERROR_CODES.FORBIDDEN);
    }

    const isPasswordValid = bcrypt.compareSync(password, user.password_hash);
    if (!isPasswordValid) {
      throw new AppError('Invalid email or password.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.INVALID_CREDENTIALS);
    }

    // Check if seller
    let sellerProfile = null;
    if (user.role === 'SELLER') {
      sellerProfile = db.prepare('SELECT * FROM sellers WHERE user_id = ?').get(user.id);
    }

    const payload = { userId: user.id, email: user.email, role: user.role };
    const accessToken = generateAccessToken(payload);
    const refreshToken = generateRefreshToken(payload);

    return {
      user: {
        id: user.id,
        email: user.email,
        firstName: user.first_name,
        lastName: user.last_name,
        role: user.role,
        sellerProfile
      },
      accessToken,
      refreshToken
    };
  }

  static refreshSession(refreshToken) {
    if (!refreshToken) {
      throw new AppError('Refresh token required.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.UNAUTHORIZED);
    }

    try {
      const decoded = verifyRefreshToken(refreshToken);
      const user = db.prepare('SELECT id, email, role, status FROM users WHERE id = ?').get(decoded.userId);
      if (!user || user.status !== 'ACTIVE') {
        throw new AppError('Invalid refresh session.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.UNAUTHORIZED);
      }

      const payload = { userId: user.id, email: user.email, role: user.role };
      const newAccessToken = generateAccessToken(payload);
      return { accessToken: newAccessToken };
    } catch (err) {
      throw new AppError('Expired or invalid refresh token.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.UNAUTHORIZED);
    }
  }

  static getUserProfile(userId) {
    const user = db.prepare('SELECT id, email, first_name, last_name, phone, role, is_verified, created_at FROM users WHERE id = ?').get(userId);
    if (!user) {
      throw new AppError('User profile not found.', HTTP_STATUS.NOT_FOUND, ERROR_CODES.RESOURCE_NOT_FOUND);
    }

    let sellerProfile = null;
    if (user.role === 'SELLER') {
      sellerProfile = db.prepare('SELECT * FROM sellers WHERE user_id = ?').get(user.id);
    }

    const addresses = db.prepare('SELECT * FROM addresses WHERE user_id = ?').all(user.id);

    return {
      user,
      sellerProfile,
      addresses
    };
  }
}

module.exports = AuthService;
