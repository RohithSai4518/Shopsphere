const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');
const AppError = require('../utils/appError');

const requestCounts = new Map();

function rateLimiter(options = {}) {
  const windowMs = options.windowMs || 15 * 60 * 1000; // 15 minutes default
  const maxRequests = options.maxRequests || 100; // 100 requests per window

  return (req, res, next) => {
    const ip = req.ip || req.connection.remoteAddress || 'unknown-ip';
    const now = Date.now();

    let record = requestCounts.get(ip);

    if (!record || now - record.startTime > windowMs) {
      record = { count: 1, startTime: now };
      requestCounts.set(ip, record);
    } else {
      record.count += 1;
    }

    if (record.count > maxRequests) {
      return next(new AppError(
        'Too many requests from this IP. Please try again later.',
        HTTP_STATUS.TOO_MANY_REQUESTS,
        ERROR_CODES.RATE_LIMIT_EXCEEDED
      ));
    }

    next();
  };
}

module.exports = rateLimiter;
