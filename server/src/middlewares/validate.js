const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

function validate(schema) {
  return (req, res, next) => {
    try {
      const parsed = schema.parse({
        body: req.body,
        query: req.query,
        params: req.params
      });
      req.body = parsed.body || req.body;
      req.query = parsed.query || req.query;
      req.params = parsed.params || req.params;
      next();
    } catch (err) {
      if (err.errors) {
        const details = err.errors.map(e => ({
          field: e.path.join('.'),
          issue: e.message
        }));
        return next(new AppError('Request validation failed.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.VALIDATION_ERROR, details));
      }
      next(err);
    }
  };
}

module.exports = validate;
