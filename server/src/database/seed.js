const db = require('./db');
const bcrypt = require('bcryptjs');

function seedDatabase() {
  console.log('🌱 Seeding ShopSphere Database with Complete Synthetic Marketplace Data...');

  const passwordHash = bcrypt.hashSync('DemoUserPass123!', 10);

  db.transaction(() => {
    // 1. Roles & Permissions
    const adminRoleId = 'role_admin';
    const sellerRoleId = 'role_seller';
    const customerRoleId = 'role_customer';

    db.prepare("INSERT OR REPLACE INTO roles (id, name, description, is_system_role) VALUES (?, 'ADMIN', 'Platform Governance Administrator', 1)").run(adminRoleId);
    db.prepare("INSERT OR REPLACE INTO roles (id, name, description, is_system_role) VALUES (?, 'SELLER', 'Verified Marketplace Seller Merchant', 1)").run(sellerRoleId);
    db.prepare("INSERT OR REPLACE INTO roles (id, name, description, is_system_role) VALUES (?, 'CUSTOMER', 'Standard Marketplace Shopper', 1)").run(customerRoleId);

    // 2. Users
    const adminId = 'usr_admin_001';
    const sellerId = 'usr_seller_001';
    const customerId = 'usr_customer_001';

    const insertUser = db.prepare(`
      INSERT OR REPLACE INTO users (id, email, password_hash, first_name, last_name, phone, role, is_verified, status)
      VALUES (?, ?, ?, ?, ?, ?, ?, 1, 'ACTIVE')
    `);

    insertUser.run(adminId, 'admin@shopsphere.local', passwordHash, 'Platform', 'Administrator', '+15550001111', 'ADMIN');
    insertUser.run(sellerId, 'seller@apextech.local', passwordHash, 'Alex', 'Merchant', '+15550002222', 'SELLER');
    insertUser.run(customerId, 'customer@example.local', passwordHash, 'Jane', 'Shopper', '+15550003333', 'CUSTOMER');

    // 3. User Roles Assignment
    db.prepare('INSERT OR REPLACE INTO user_roles (user_id, role_id) VALUES (?, ?)').run(adminId, adminRoleId);
    db.prepare('INSERT OR REPLACE INTO user_roles (user_id, role_id) VALUES (?, ?)').run(sellerId, sellerRoleId);
    db.prepare('INSERT OR REPLACE INTO user_roles (user_id, role_id) VALUES (?, ?)').run(customerId, customerRoleId);

    // 4. User Preferences
    db.prepare(`
      INSERT OR REPLACE INTO user_preferences (user_id, email_notifications, sms_notifications, promotional_emails, theme, currency)
      VALUES (?, 1, 1, 1, 'DARK', 'USD')
    `).run(customerId);

    // 5. Seller Profile
    const sellerProfileId = 'sel_apex_001';
    db.prepare(`
      INSERT OR REPLACE INTO sellers (id, user_id, business_name, business_email, business_phone, tax_id, status, commission_rate, rating_avg)
      VALUES (?, ?, ?, ?, ?, ?, 'APPROVED', 8.50, 4.85)
    `).run(sellerProfileId, sellerId, 'Apex Electronics Store', 'contact@apextech.local', '+15550002222', 'TAX-998877');

    // 6. Addresses
    const insertAddr = db.prepare(`
      INSERT OR REPLACE INTO addresses (id, user_id, address_type, full_name, street_address_1, street_address_2, city, state, postal_code, country, is_default)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    `);
    insertAddr.run('addr_cust_01', customerId, 'SHIPPING', 'Jane Shopper', '100 Synthetic Way', 'Apt 4B', 'Innovation City', 'CA', '90210', 'United States');
    insertAddr.run('addr_cust_02', customerId, 'BILLING', 'Jane Shopper', '100 Synthetic Way', 'Apt 4B', 'Innovation City', 'CA', '90210', 'United States');

    // 7. Brands
    const brandApex = 'brd_apex_01';
    const brandSonic = 'brd_sonic_02';
    db.prepare("INSERT OR REPLACE INTO brands (id, name, slug, description) VALUES (?, 'ApexTech', 'apextech', 'High-performance computing and gadgets')").run(brandApex);
    db.prepare("INSERT OR REPLACE INTO brands (id, name, slug, description) VALUES (?, 'SonicWave', 'sonicwave', 'Premium audio, headphones, and wireless sound')").run(brandSonic);

    // 8. Categories
    const catElectronics = 'cat_elec_01';
    const catLaptops = 'cat_laptops_02';
    const catAudio = 'cat_audio_03';
    const catHome = 'cat_home_04';

    const insertCat = db.prepare(`
      INSERT OR REPLACE INTO categories (id, parent_id, name, slug, description, display_order, is_active)
      VALUES (?, ?, ?, ?, ?, ?, 1)
    `);
    insertCat.run(catElectronics, null, 'Electronics & Gadgets', 'electronics', 'High performance consumer electronics and devices', 1);
    insertCat.run(catLaptops, catElectronics, 'Laptops & Computers', 'laptops', 'Ultra-portable laptops, workstation laptops, and desktops', 2);
    insertCat.run(catAudio, catElectronics, 'Headphones & Audio', 'audio', 'Noise-canceling headphones, wireless earbuds, and speakers', 3);
    insertCat.run(catHome, null, 'Home & Kitchen', 'home-kitchen', 'Smart home appliances, kitchenware, and furniture', 4);

    // 9. Products
    const prodLaptop = 'prd_laptop_01';
    const prodEarbuds = 'prd_earbuds_02';

    const insertProd = db.prepare(`
      INSERT OR REPLACE INTO products (id, seller_id, category_id, brand_id, name, slug, brand, description, base_price, discount_percent, tax_rate, status)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'PUBLISHED')
    `);
    insertProd.run(
      prodLaptop, sellerProfileId, catLaptops, brandApex,
      'ApexPro X15 Ultra Laptop', 'apexpro-x15-ultra-laptop', 'ApexTech',
      'The ApexPro X15 features a 15.6-inch QHD OLED display, 16-core processor, 32GB DDR5 RAM, and 1TB NVMe SSD.',
      1499.99, 10.00, 8.25
    );
    insertProd.run(
      prodEarbuds, sellerProfileId, catAudio, brandSonic,
      'SonicWave Pro Wireless Noise-Canceling Earbuds', 'sonicwave-pro-wireless-earbuds', 'SonicWave',
      'Active Noise Cancellation (ANC) with 36-hour total playback battery life, IPX7 water resistance, and studio mic quality.',
      199.99, 15.00, 8.25
    );

    // 10. Product Specifications
    const insertSpec = db.prepare('INSERT OR REPLACE INTO product_specifications (id, product_id, spec_key, spec_value, display_order) VALUES (?, ?, ?, ?, ?)');
    insertSpec.run('spec_01', prodLaptop, 'Processor', '16-Core Ultra CPU 5.2GHz', 1);
    insertSpec.run('spec_02', prodLaptop, 'RAM', '32GB DDR5 5600MHz', 2);
    insertSpec.run('spec_03', prodLaptop, 'Storage', '1TB PCIe Gen4 NVMe SSD', 3);
    insertSpec.run('spec_04', prodLaptop, 'Display', '15.6" QHD OLED 120Hz 100% DCI-P3', 4);

    // 11. Variants
    const varLaptop1 = 'var_laptop_01_32gb';
    const varEarbudsBlack = 'var_earbuds_blk';

    const insertVariant = db.prepare(`
      INSERT OR REPLACE INTO product_variants (id, product_id, sku, variant_name, price_override, attributes_json, weight_kg, is_default)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `);
    insertVariant.run(varLaptop1, prodLaptop, 'APEX-X15-32GB-1TB', '32GB RAM / 1TB SSD - Space Gray', 1499.99, JSON.stringify({ RAM: '32GB', Storage: '1TB', Color: 'Space Gray' }), 1.85, 1);
    insertVariant.run(varEarbudsBlack, prodEarbuds, 'SONIC-EARBUD-BLK', 'Midnight Black', 199.99, JSON.stringify({ Color: 'Midnight Black' }), 0.25, 1);

    // 12. Product Images
    const insertImg = db.prepare('INSERT OR REPLACE INTO product_images (id, product_id, image_url, alt_text, display_order, is_primary) VALUES (?, ?, ?, ?, ?, ?)');
    insertImg.run('img_laptop_01', prodLaptop, 'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=600&q=80', 'ApexPro X15 Ultra Laptop', 1, 1);
    insertImg.run('img_earbuds_01', prodEarbuds, 'https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=600&q=80', 'SonicWave Pro Earbuds', 1, 1);

    // 13. Product Bundles
    db.prepare(`
      INSERT OR REPLACE INTO product_bundles (id, name, slug, description, bundle_price, discount_amount, is_active)
      VALUES ('bnd_pro_creator', 'Pro Creator Executive Tech Bundle', 'pro-creator-tech-bundle', 'Includes ApexPro X15 Laptop + SonicWave Pro ANC Earbuds at an exclusive combined bundle price.', 1599.99, 100.00, 1)
    `).run();

    // 14. Inventory & Transactions Ledger
    const insertInv = db.prepare(`
      INSERT OR REPLACE INTO inventory (id, variant_id, quantity_on_hand, quantity_reserved, reorder_threshold)
      VALUES (?, ?, ?, 0, 5)
    `);
    insertInv.run('inv_01', varLaptop1, 45);
    insertInv.run('inv_02', varEarbudsBlack, 120);

    db.prepare(`
      INSERT OR REPLACE INTO inventory_transactions (id, variant_id, transaction_type, quantity, reference_type, notes)
      VALUES ('inv_tx_01', 'var_laptop_01_32gb', 'RECEIPT', 50, 'RESTOCK', 'Initial factory inventory stock receipt')
    `).run();

    // 15. Wishlists & Price Alerts
    db.prepare("INSERT OR REPLACE INTO wishlists (id, user_id, name, is_public) VALUES ('wsh_cust_01', 'usr_customer_001', 'My Executive Wishlist', 0)").run();
    db.prepare("INSERT OR REPLACE INTO wishlist_items (id, wishlist_id, product_id) VALUES ('wshi_01', 'wsh_cust_01', 'prd_laptop_01')").run();
    db.prepare("INSERT OR REPLACE INTO price_alerts (id, user_id, product_id, target_price) VALUES ('pal_01', 'usr_customer_001', 'prd_laptop_01', 1350.00)").run();

    // 16. Coupons & Promotions
    const insertCoupon = db.prepare(`
      INSERT OR REPLACE INTO coupons (id, code, discount_type, discount_value, min_order_subtotal, usage_limit, per_user_limit, starts_at, expires_at, is_active)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
    `);
    insertCoupon.run('cpn_welcome10', 'WELCOME10', 'PERCENTAGE', 10.00, 50.00, 1000, 1, '2026-01-01T00:00:00Z', '2027-01-01T00:00:00Z');
    insertCoupon.run('cpn_flat25', 'SAVE25', 'FIXED', 25.00, 150.00, 500, 1, '2026-01-01T00:00:00Z', '2027-01-01T00:00:00Z');

    // 17. Seed Order & Order Items
    db.prepare(`
      INSERT INTO orders (id, order_number, user_id, status, subtotal, tax_amount, shipping_amount, discount_amount, total_amount, coupon_id, shipping_address_json, billing_address_json)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, null, '{}', '{}')
    `).run('ord_seed_01', 'ORD-20260101-1001', 'usr_customer_001', 'CONFIRMED', 1349.99, 111.37, 0.00, 135.00, 1326.36);
    db.prepare(`
      INSERT INTO order_items (id, order_id, variant_id, seller_id, unit_price, discount_amount, tax_amount, quantity, total_price)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).run('ori_seed_item_01', 'ord_seed_01', 'var_laptop_01_32gb', 'sel_apex_001', 1349.99, 135.00, 111.37, 1, 1349.99);

    // 18. Reviews & Review Votes
    const insertReview = db.prepare(`
      INSERT OR REPLACE INTO reviews (id, product_id, user_id, rating, title, comment, is_verified_purchase, status, helpful_votes)
      VALUES (?, ?, ?, ?, ?, ?, 1, 'APPROVED', 12)
    `);
    insertReview.run('rev_01', prodLaptop, customerId, 5, 'Exceptional Workstation Laptop', 'Superb build quality, blazing fast render times, and accurate color screen.', 1);
    insertReview.run('rev_02', prodEarbuds, customerId, 5, 'Great ANC and Battery Life', 'Noise cancellation works amazingly during flights and battery lasts all week.', 1);

    // 18. Support Tickets
    db.prepare(`
      INSERT OR REPLACE INTO support_tickets (id, ticket_number, user_id, subject, category, priority, status)
      VALUES ('tkt_001', 'TKT-10092', 'usr_customer_001', 'Inquiry regarding warranty extension', 'PRODUCT', 'MEDIUM', 'OPEN')
    `).run();
    db.prepare(`
      INSERT OR REPLACE INTO support_messages (id, ticket_id, sender_id, message, is_internal_note)
      VALUES ('msg_001', 'tkt_001', 'usr_customer_001', 'Hello, does the ApexPro X15 come with international manufacturer warranty coverage?', 0)
    `).run();

    // 19. Security Audit Log
    db.prepare(`
      INSERT OR REPLACE INTO security_audit_logs (id, user_id, action, module, entity_type, entity_id, ip_address)
      VALUES ('aud_001', 'usr_admin_001', 'SYSTEM_INITIALIZATION', 'SYSTEM', 'DATABASE', 'shopsphere_db', '127.0.0.1')
    `).run();

  })();

  console.log('✅ Synthetic database seeding completed with 36 relational entities.');
}

if (require.main === module) {
  try {
    seedDatabase();
  } catch (error) {
    console.error('❌ Seeding failed:', error);
    process.exit(1);
  }
}

module.exports = { seedDatabase };
