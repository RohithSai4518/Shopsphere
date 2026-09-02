const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const path = require('path');

const rateLimiter = require('./middlewares/rateLimiter');
const errorHandler = require('./middlewares/errorHandler');
const logger = require('./utils/logger');
const HTTP_STATUS = require('./constants/statusCodes');

const authRoutes = require('./routes/authRoutes');
const catalogRoutes = require('./routes/catalogRoutes');
const cartRoutes = require('./routes/cartRoutes');
const orderRoutes = require('./routes/orderRoutes');
const sellerRoutes = require('./routes/sellerRoutes');
const adminRoutes = require('./routes/adminRoutes');
const accountRoutes = require('./routes/accountRoutes');
const wishlistRoutes = require('./routes/wishlistRoutes');
const supportRoutes = require('./routes/supportRoutes');
const returnsRoutes = require('./routes/returnsRoutes');
const rbacRoutes = require('./routes/rbacRoutes');
const analyticsRoutes = require('./routes/analyticsRoutes');

const app = express();
const PORT = process.env.PORT || 5000;
const API_PREFIX = process.env.API_PREFIX || '/api/v1';

// Security Middlewares
app.use(helmet());
app.use(cors({
  origin: process.env.CLIENT_URL || 'http://localhost:3000',
  credentials: true
}));

app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// Apply rate limiting
app.use(rateLimiter({ windowMs: 15 * 60 * 1000, maxRequests: 300 }));

// Logging Middleware
app.use((req, res, next) => {
  logger.info(`${req.method} ${req.originalUrl}`);
  next();
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.status(HTTP_STATUS.OK).json({
    status: 'UP',
    service: 'ShopSphere Core Marketplace Engine',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.use(`${API_PREFIX}/auth`, authRoutes);
app.use(`${API_PREFIX}`, catalogRoutes);
app.use(`${API_PREFIX}/cart`, cartRoutes);
app.use(`${API_PREFIX}/orders`, orderRoutes);
app.use(`${API_PREFIX}/seller`, sellerRoutes);
app.use(`${API_PREFIX}/admin`, adminRoutes);
app.use(`${API_PREFIX}/account`, accountRoutes);
app.use(`${API_PREFIX}/wishlist`, wishlistRoutes);
app.use(`${API_PREFIX}/support`, supportRoutes);
app.use(`${API_PREFIX}/returns`, returnsRoutes);
app.use(`${API_PREFIX}/rbac`, rbacRoutes);
app.use(`${API_PREFIX}/analytics`, analyticsRoutes);

// 404 Route Handler
app.use((req, res, next) => {
  res.status(HTTP_STATUS.NOT_FOUND).json({
    success: false,
    error: {
      code: 'ROUTE_NOT_FOUND',
      message: `The requested endpoint ${req.originalUrl} does not exist on this server.`
    },
    timestamp: new Date().toISOString()
  });
});

// Global Centralized Error Handler
app.use(errorHandler);

if (require.main === module) {
  app.listen(PORT, () => {
    logger.info(`🚀 ShopSphere Server running in ${process.env.NODE_ENV || 'development'} mode on port ${PORT}`);
    logger.info(`🌐 Base API URL: http://localhost:${PORT}${API_PREFIX}`);
  });
}

module.exports = app;
