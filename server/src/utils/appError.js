const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class AppError extends Error {
  constructor(message, statusCode = HTTP_STATUS.BAD_REQUEST, errorCode = ERROR_CODES.VALIDATION_ERROR, details = []) {
    super(message);
    this.name = this.constructor.name;
    this.statusCode = statusCode;
    this.errorCode = errorCode;
    this.details = details;
    this.isOperational = true;
    Error.captureStackTrace(this, this.constructor);
  }
}

module.exports = AppError;
