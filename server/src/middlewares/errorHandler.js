const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');
const logger = require('../utils/logger');

function errorHandler(err, req, res, next) {
  const statusCode = err.statusCode || HTTP_STATUS.INTERNAL_SERVER_ERROR;
  const errorCode = err.errorCode || ERROR_CODES.INTERNAL_ERROR;
  
  // Log full internal error for server monitoring
  logger.error(`${req.method} ${req.originalUrl} - ${err.message}`, {
    statusCode,
    errorCode,
    stack: process.env.NODE_ENV === 'development' ? err.stack : undefined
  });

  // Prepare safe response envelope
  const response = {
    success: false,
    error: {
      code: errorCode,
      message: err.isOperational ? err.message : 'An unexpected server error occurred. Please try again later.',
      details: err.details || []
    },
    timestamp: new Date().toISOString()
  };

  res.status(statusCode).json(response);
}

module.exports = errorHandler;
