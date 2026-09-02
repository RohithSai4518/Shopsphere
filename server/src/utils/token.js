const jwt = require('jsonwebtoken');

const JWT_SECRET = process.env.JWT_SECRET || 'shopsphere_dev_secret_key_change_in_prod';
const REFRESH_SECRET = process.env.REFRESH_TOKEN_SECRET || 'shopsphere_dev_refresh_secret_key';

function generateAccessToken(payload) {
  return jwt.sign(payload, JWT_SECRET, { expiresIn: process.env.JWT_EXPIRES_IN || '15m' });
}

function generateRefreshToken(payload) {
  return jwt.sign(payload, REFRESH_SECRET, { expiresIn: process.env.REFRESH_TOKEN_EXPIRES_IN || '7d' });
}

function verifyAccessToken(token) {
  return jwt.verify(token, JWT_SECRET);
}

function verifyRefreshToken(token) {
  return jwt.verify(token, REFRESH_SECRET);
}

module.exports = {
  generateAccessToken,
  generateRefreshToken,
  verifyAccessToken,
  verifyRefreshToken
};
