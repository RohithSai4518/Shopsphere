const AuthService = require('../services/authService');
const HTTP_STATUS = require('../constants/statusCodes');

class AuthController {
  static register(req, res, next) {
    try {
      const result = AuthService.registerUser(req.body);
      
      // Set secure HTTP-only refresh cookie
      res.cookie('refreshToken', result.refreshToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
      });

      res.status(HTTP_STATUS.CREATED).json({
        success: true,
        data: {
          user: result.user,
          accessToken: result.accessToken
        },
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static login(req, res, next) {
    try {
      const result = AuthService.loginUser(req.body);

      res.cookie('refreshToken', result.refreshToken, {
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000
      });

      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: {
          user: result.user,
          accessToken: result.accessToken
        },
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static refreshToken(req, res, next) {
    try {
      const refreshToken = req.cookies.refreshToken || req.body.refreshToken;
      const result = AuthService.refreshSession(refreshToken);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: { accessToken: result.accessToken },
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static logout(req, res, next) {
    try {
      res.clearCookie('refreshToken');
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: { message: 'Logged out successfully.' },
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }

  static getProfile(req, res, next) {
    try {
      const profile = AuthService.getUserProfile(req.user.userId);
      res.status(HTTP_STATUS.OK).json({
        success: true,
        data: profile,
        meta: { timestamp: new Date().toISOString() }
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = AuthController;
