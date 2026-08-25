const assert = require('assert');
const test = require('node:test');

process.env.NODE_ENV = 'test';
process.env.DB_FILE = './data/test_e2e.json';

const AuthService = require('../../server/src/services/authService');
const CatalogService = require('../../server/src/services/catalogService');
const CartService = require('../../server/src/services/cartService');
const OrderService = require('../../server/src/services/orderService');
const SellerService = require('../../server/src/services/sellerService');
const AdminService = require('../../server/src/services/adminService');
const AuditService = require('../../server/src/services/auditService');
const { seedDatabase } = require('../../server/src/database/seed.js');

test('End-to-End Marketplace Workflows (Customer, Seller, Admin)', async (t) => {
  seedDatabase();

  let customerEmail = `e2e_cust_${Date.now()}@example.local`;
  let customerUser = null;
  let sellerUser = null;

  await t.test('Workflow 1: Customer Register -> Browse -> Cart -> Checkout -> Order', () => {
    // 1. Customer Register
    const reg = AuthService.registerUser({
      email: customerEmail,
      password: 'CustomerPass123!',
      firstName: 'E2E',
      lastName: 'Customer',
      role: 'CUSTOMER'
    });
    customerUser = reg.user;
    assert.strictEqual(customerUser.email, customerEmail);

    // 2. Browse Products
    const catalog = CatalogService.getProducts({ keyword: 'ApexPro' });
    assert.ok(catalog.products.length > 0);

    // 3. Add to Cart
    CartService.clearCart(customerUser.id);
    CartService.addToCart(customerUser.id, 'var_laptop_01_32gb', 1);
    const cart = CartService.getCart(customerUser.id);
    assert.strictEqual(cart.items.length, 1);

    // 4. Multi-step Checkout Order
    const order = OrderService.createOrder(customerUser.id, {
      shippingAddress: {
        fullName: 'E2E Customer',
        streetAddress1: '100 E2E Way',
        city: 'San Francisco',
        state: 'CA',
        postalCode: '94105',
        country: 'United States'
      },
      couponCode: 'WELCOME10',
      paymentMethodToken: 'mock_token_success'
    });

    assert.strictEqual(order.status, 'CONFIRMED');
    assert.ok(order.orderNumber.startsWith('ORD-'));
  });

  await t.test('Workflow 2: Seller Register -> Create Product -> Dashboard -> Fulfill Item', () => {
    const sellerEmail = `e2e_seller_${Date.now()}@example.local`;
    const reg = AuthService.registerUser({
      email: sellerEmail,
      password: 'SellerPass123!',
      firstName: 'E2E',
      lastName: 'Merchant',
      role: 'SELLER',
      businessName: 'E2E Tech Store'
    });
    sellerUser = reg.user;
    assert.strictEqual(sellerUser.role, 'SELLER');

    // Approve Seller profile for test
    AdminService.approveSeller(sellerUser.sellerProfile.sellerId, { action: 'APPROVE' });

    // Create New Merchant Product
    const newProd = CatalogService.createProduct(sellerUser.sellerProfile.sellerId, {
      name: 'E2E Ultra Wireless Mouse',
      categoryId: 'cat_elec_01',
      basePrice: 49.99,
      description: 'Precision ergonomic wireless gaming mouse.',
      stockQuantity: 100
    });
    assert.ok(newProd.productId);

    // Fulfill Order Item
    const fulfillment = SellerService.fulfillOrderItem('usr_seller_001', 'ori_seed_item_01', {
      carrier: 'Express Post',
      trackingNumber: 'TRK-E2E-9988'
    });
    assert.strictEqual(fulfillment.status, 'SHIPPED');
  });

  await t.test('Workflow 3: Admin Analytics -> Approve Seller -> Security Audit Log', () => {
    const analytics = AdminService.getPlatformAnalytics();
    assert.ok(analytics.metrics.totalProducts >= 2);

    // Record Security Audit Log
    AuditService.logEvent('usr_admin_001', 'E2E_WORKFLOW_TEST', 'ADMIN', 'SYSTEM', 'e2e_node_test', '127.0.0.1');

    const logs = AuditService.getAuditLogs(1, 10);
    assert.ok(logs.logs.length > 0);
  });
});
