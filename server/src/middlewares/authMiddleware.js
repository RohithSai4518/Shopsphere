const { verifyAccessToken } = require('../utils/token');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

function authenticate(req, res, next) {
  let token = null;
  const authHeader = req.headers.authorization;

  if (authHeader && authHeader.startsWith('Bearer ')) {
    token = authHeader.split(' ')[1];
  } else if (req.cookies && req.cookies.accessToken) {
    token = req.cookies.accessToken;
  }

  if (!token) {
    return next(new AppError('Authentication token required. Please log in.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.UNAUTHORIZED));
  }

  try {
    const decoded = verifyAccessToken(token);
    req.user = decoded;
    next();
  } catch (err) {
    if (err.name === 'TokenExpiredError') {
      return next(new AppError('Session expired. Please log in again.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.TOKEN_EXPIRED));
    }
    return next(new AppError('Invalid authentication token.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.UNAUTHORIZED));
  }
}

function authorize(...allowedRoles) {
  return (req, res, next) => {
    if (!req.user || !req.user.role) {
      return next(new AppError('User profile not attached.', HTTP_STATUS.UNAUTHORIZED, ERROR_CODES.UNAUTHORIZED));
    }

    if (!allowedRoles.includes(req.user.role)) {
      return next(new AppError(
        `Access denied. Requires one of the following roles: ${allowedRoles.join(', ')}`,
        HTTP_STATUS.FORBIDDEN,
        ERROR_CODES.FORBIDDEN
      ));
    }

    next();
  };
}

module.exports = {
  authenticate,
  authorize
};
