const db = require('../database/db');
const AppError = require('../utils/appError');
const HTTP_STATUS = require('../constants/statusCodes');
const ERROR_CODES = require('../constants/errorCodes');

class PromotionService {
  static getActiveCampaigns() {
    return db.prepare('SELECT * FROM promotional_campaigns WHERE is_active = 1 ORDER BY starts_at DESC').all();
  }

  static createCampaign({ name, bannerUrl, discountPercent, startsAt, expiresAt }) {
    if (!name || discountPercent <= 0 || discountPercent > 100) {
      throw new AppError('Invalid campaign parameters.', HTTP_STATUS.BAD_REQUEST, ERROR_CODES.VALIDATION_ERROR);
    }

    const campaignId = `cmp_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, '-');

    db.prepare(`
      INSERT INTO promotional_campaigns (id, name, slug, banner_url, discount_percent, starts_at, expires_at, is_active)
      VALUES (?, ?, ?, ?, ?, ?, ?, 1)
    `).run(campaignId, name, slug, bannerUrl || null, discountPercent, startsAt || new Date().toISOString(), expiresAt || new Date(Date.now() + 30*24*60*60*1000).toISOString());

    return { campaignId, name, discountPercent };
  }
}

module.exports = PromotionService;
