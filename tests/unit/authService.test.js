const assert = require('assert');
const test = require('node:test');

// Load environment variables for test environment
process.env.NODE_ENV = 'test';
process.env.DB_FILE = './data/test_authService.json';

const AuthService = require('../../server/src/services/authService');
const db = require('../../server/src/database/db');

test('AuthService Unit Tests', async (t) => {

  await t.test('1. Should register a new customer successfully', () => {
    const testEmail = `test_customer_${Date.now()}@example.local`;
    const result = AuthService.registerUser({
      email: testEmail,
      password: 'SecurePassword123!',
      firstName: 'Alice',
      lastName: 'Tester',
      role: 'CUSTOMER'
    });

    assert.strictEqual(result.user.email, testEmail);
    assert.strictEqual(result.user.role, 'CUSTOMER');
    assert.ok(result.accessToken);
    assert.ok(result.refreshToken);
  });

  await t.test('2. Should reject duplicate email registration', () => {
    const duplicateEmail = `dup_${Date.now()}@example.local`;
    AuthService.registerUser({
      email: duplicateEmail,
      password: 'Password123!',
      firstName: 'Bob',
      lastName: 'Dup',
      role: 'CUSTOMER'
    });

    assert.throws(() => {
      AuthService.registerUser({
        email: duplicateEmail,
        password: 'Password123!',
        firstName: 'Bob',
        lastName: 'Dup',
        role: 'CUSTOMER'
      });
    }, (err) => err.statusCode === 409);
  });

  await t.test('3. Should authenticate valid user credentials', () => {
    const loginEmail = `login_${Date.now()}@example.local`;
    AuthService.registerUser({
      email: loginEmail,
      password: 'LoginPass123!',
      firstName: 'Charlie',
      lastName: 'Login',
      role: 'CUSTOMER'
    });

    const loginResult = AuthService.loginUser({
      email: loginEmail,
      password: 'LoginPass123!'
    });

    assert.strictEqual(loginResult.user.email, loginEmail);
    assert.ok(loginResult.accessToken);
  });

  await t.test('4. Should reject invalid login password', () => {
    const userEmail = `wrongpass_${Date.now()}@example.local`;
    AuthService.registerUser({
      email: userEmail,
      password: 'CorrectPassword123!',
      firstName: 'David',
      lastName: 'WrongPass',
      role: 'CUSTOMER'
    });

    assert.throws(() => {
      AuthService.loginUser({
        email: userEmail,
        password: 'IncorrectPassword!'
      });
    }, (err) => err.statusCode === 401);
  });
});
