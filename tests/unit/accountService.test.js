const assert = require('assert');
const test = require('node:test');

process.env.NODE_ENV = 'test';
process.env.DB_FILE = './data/test_accountService.json';

const AccountService = require('../../server/src/services/accountService');
const { seedDatabase } = require('../../server/src/database/seed.js');

test('AccountService Unit Tests', async (t) => {
  seedDatabase();

  const userId = 'usr_customer_001';

  await t.test('1. Should update customer profile information', () => {
    const updated = AccountService.updateProfile(userId, {
      firstName: 'Jane',
      lastName: 'Shopper-Updated',
      phone: '+15559998888'
    });
    assert.strictEqual(updated.last_name, 'Shopper-Updated');
    assert.strictEqual(updated.phone, '+15559998888');
  });

  await t.test('2. Should add address and set as default', () => {
    const addresses = AccountService.addAddress(userId, {
      addressType: 'SHIPPING',
      fullName: 'Jane Executive',
      streetAddress1: '500 Tech Boulevard',
      city: 'San Francisco',
      state: 'CA',
      postalCode: '94105',
      country: 'United States',
      isDefault: true
    });

    assert.ok(addresses.length > 0);
    const def = addresses.find(a => a.is_default === 1);
    assert.ok(def);
    assert.strictEqual(def.city, 'San Francisco');
  });

  await t.test('3. Should manage and update user preferences', () => {
    const prefs = AccountService.updatePreferences(userId, {
      emailNotifications: true,
      smsNotifications: true,
      promotionalEmails: false,
      theme: 'DARK',
      currency: 'USD'
    });

    assert.strictEqual(prefs.sms_notifications, 1);
    assert.strictEqual(prefs.promotional_emails, 0);
  });

  await t.test('4. Should record and retrieve recently viewed products', () => {
    AccountService.recordRecentlyViewed(userId, 'prd_laptop_01');
    const recent = AccountService.getRecentlyViewed(userId);
    assert.ok(recent.length > 0);
  });
});
