-- ============================================================================
-- SHOPSPHERE ENTERPRISE MARKETPLACE DATABASE SCHEMA
-- ============================================================================
-- Architecture: 3NF Relational Database Schema
-- Entities: 36 Tables covering Identity, RBAC, Catalog, Orders, Logistics,
-- Support, Promotions, Analytics, Auditing & Merchant Governance.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. USER ACCOUNTS & IDENTITY DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id VARCHAR(64) PRIMARY KEY,
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  phone VARCHAR(30),
  role VARCHAR(50) NOT NULL DEFAULT 'CUSTOMER',
  is_verified INTEGER NOT NULL DEFAULT 1,
  status VARCHAR(30) NOT NULL DEFAULT 'ACTIVE',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);

-- ----------------------------------------------------------------------------
-- 2. ROLE-BASED ACCESS CONTROL (RBAC) DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roles (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
  id VARCHAR(64) PRIMARY KEY,
  code VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  module VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS role_permissions (
  role_id VARCHAR(64) NOT NULL,
  permission_id VARCHAR(64) NOT NULL,
  PRIMARY KEY (role_id, permission_id),
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
  FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_roles (
  user_id VARCHAR(64) NOT NULL,
  role_id VARCHAR(64) NOT NULL,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 3. USER SESSIONS & PREFERENCES DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS user_sessions (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  token_hash VARCHAR(255) NOT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  expires_at TIMESTAMP NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS login_history (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  status VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_preferences (
  user_id VARCHAR(64) PRIMARY KEY,
  email_notifications INTEGER DEFAULT 1,
  sms_notifications INTEGER DEFAULT 0,
  promotional_emails INTEGER DEFAULT 1,
  theme VARCHAR(20) DEFAULT 'DARK',
  currency VARCHAR(10) DEFAULT 'USD',
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 4. MERCHANT & SELLER DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sellers (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL UNIQUE,
  business_name VARCHAR(255) NOT NULL,
  business_email VARCHAR(255) NOT NULL,
  business_phone VARCHAR(50),
  tax_id VARCHAR(100),
  commission_rate DECIMAL(5,2) DEFAULT 8.50,
  rating_avg DECIMAL(3,2) DEFAULT 0.00,
  status VARCHAR(30) DEFAULT 'PENDING',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_sellers_user ON sellers(user_id);
CREATE INDEX IF NOT EXISTS idx_sellers_status ON sellers(status);

-- ----------------------------------------------------------------------------
-- 5. ADDRESS BOOK MANAGEMENT DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS addresses (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  address_type VARCHAR(20) NOT NULL DEFAULT 'SHIPPING',
  full_name VARCHAR(150) NOT NULL,
  street_address_1 VARCHAR(255) NOT NULL,
  street_address_2 VARCHAR(255),
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  postal_code VARCHAR(30) NOT NULL,
  country VARCHAR(100) NOT NULL DEFAULT 'United States',
  is_default INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 6. PRODUCT CATALOG & TAXONOMY DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categories (
  id VARCHAR(64) PRIMARY KEY,
  parent_id VARCHAR(64),
  name VARCHAR(100) NOT NULL,
  slug VARCHAR(100) NOT NULL UNIQUE,
  description TEXT,
  icon_url VARCHAR(255),
  is_active INTEGER DEFAULT 1,
  display_order INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS brands (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  logo_url VARCHAR(255),
  website VARCHAR(255),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
  id VARCHAR(64) PRIMARY KEY,
  seller_id VARCHAR(64) NOT NULL,
  category_id VARCHAR(64) NOT NULL,
  brand_id VARCHAR(64),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) NOT NULL UNIQUE,
  brand VARCHAR(100),
  description TEXT,
  base_price DECIMAL(10,2) NOT NULL,
  discount_percent DECIMAL(5,2) DEFAULT 0.00,
  tax_rate DECIMAL(5,2) DEFAULT 8.25,
  status VARCHAR(30) DEFAULT 'PUBLISHED',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (seller_id) REFERENCES sellers(id),
  FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE INDEX IF NOT EXISTS idx_products_seller ON products(seller_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_products_slug ON products(slug);

CREATE TABLE IF NOT EXISTS product_variants (
  id VARCHAR(64) PRIMARY KEY,
  product_id VARCHAR(64) NOT NULL,
  sku VARCHAR(100) NOT NULL UNIQUE,
  variant_name VARCHAR(100) NOT NULL,
  price_override DECIMAL(10,2),
  attributes_json TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_specifications (
  id VARCHAR(64) PRIMARY KEY,
  product_id VARCHAR(64) NOT NULL,
  spec_key VARCHAR(100) NOT NULL,
  spec_value VARCHAR(255) NOT NULL,
  display_group VARCHAR(100) DEFAULT 'General',
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_images (
  id VARCHAR(64) PRIMARY KEY,
  product_id VARCHAR(64) NOT NULL,
  image_url TEXT NOT NULL,
  is_primary INTEGER DEFAULT 0,
  display_order INTEGER DEFAULT 0,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS product_bundles (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  discount_percentage DECIMAL(5,2) DEFAULT 10.00,
  is_active INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS bundle_items (
  bundle_id VARCHAR(64) NOT NULL,
  product_id VARCHAR(64) NOT NULL,
  PRIMARY KEY (bundle_id, product_id),
  FOREIGN KEY (bundle_id) REFERENCES product_bundles(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 7. INVENTORY & WAREHOUSE LOGISTICS DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS warehouse_locations (
  id VARCHAR(64) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  code VARCHAR(30) NOT NULL UNIQUE,
  address VARCHAR(255) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state VARCHAR(100) NOT NULL,
  country VARCHAR(100) NOT NULL DEFAULT 'United States'
);

CREATE TABLE IF NOT EXISTS inventory (
  id VARCHAR(64) PRIMARY KEY,
  variant_id VARCHAR(64) NOT NULL UNIQUE,
  quantity_on_hand INTEGER NOT NULL DEFAULT 0,
  quantity_reserved INTEGER NOT NULL DEFAULT 0,
  reorder_threshold INTEGER DEFAULT 5,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (variant_id) REFERENCES product_variants(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS inventory_transactions (
  id VARCHAR(64) PRIMARY KEY,
  variant_id VARCHAR(64) NOT NULL,
  transaction_type VARCHAR(30) NOT NULL,
  quantity INTEGER NOT NULL,
  reference_type VARCHAR(50),
  reference_id VARCHAR(64),
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (variant_id) REFERENCES product_variants(id)
);

-- ----------------------------------------------------------------------------
-- 8. SHOPPING CART & WISHLIST DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cart_items (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  variant_id VARCHAR(64) NOT NULL,
  quantity INTEGER NOT NULL DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (variant_id) REFERENCES product_variants(id)
);

CREATE INDEX IF NOT EXISTS idx_cart_user ON cart_items(user_id);

CREATE TABLE IF NOT EXISTS wishlists (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  name VARCHAR(100) NOT NULL DEFAULT 'My Wishlist',
  is_public INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS wishlist_items (
  id VARCHAR(64) PRIMARY KEY,
  wishlist_id VARCHAR(64) NOT NULL,
  product_id VARCHAR(64) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (wishlist_id) REFERENCES wishlists(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS price_alerts (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64) NOT NULL,
  product_id VARCHAR(64) NOT NULL,
  target_price DECIMAL(10,2) NOT NULL,
  is_triggered INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 9. PROMOTIONS, COUPONS & CAMPAIGNS DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS coupons (
  id VARCHAR(64) PRIMARY KEY,
  code VARCHAR(50) NOT NULL UNIQUE,
  discount_type VARCHAR(20) NOT NULL,
  discount_value DECIMAL(10,2) NOT NULL,
  min_order_subtotal DECIMAL(10,2) DEFAULT 0.00,
  usage_limit INTEGER DEFAULT 1000,
  per_user_limit INTEGER DEFAULT 1,
  starts_at TIMESTAMP NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  is_active INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS promotional_campaigns (
  id VARCHAR(64) PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  banner_url TEXT,
  discount_percentage DECIMAL(5,2) DEFAULT 15.00,
  starts_at TIMESTAMP NOT NULL,
  expires_at TIMESTAMP NOT NULL,
  is_active INTEGER DEFAULT 1
);

-- ----------------------------------------------------------------------------
-- 10. ORDERS & CHECKOUT DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
  id VARCHAR(64) PRIMARY KEY,
  order_number VARCHAR(50) NOT NULL UNIQUE,
  user_id VARCHAR(64) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
  subtotal DECIMAL(10,2) NOT NULL,
  tax_amount DECIMAL(10,2) NOT NULL,
  shipping_amount DECIMAL(10,2) NOT NULL,
  discount_amount DECIMAL(10,2) DEFAULT 0.00,
  total_amount DECIMAL(10,2) NOT NULL,
  coupon_id VARCHAR(64),
  shipping_address_json TEXT NOT NULL,
  billing_address_json TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(status);

CREATE TABLE IF NOT EXISTS order_items (
  id VARCHAR(64) PRIMARY KEY,
  order_id VARCHAR(64) NOT NULL,
  variant_id VARCHAR(64) NOT NULL,
  seller_id VARCHAR(64) NOT NULL,
  unit_price DECIMAL(10,2) NOT NULL,
  discount_amount DECIMAL(10,2) DEFAULT 0.00,
  tax_amount DECIMAL(10,2) DEFAULT 0.00,
  quantity INTEGER NOT NULL,
  total_price DECIMAL(10,2) NOT NULL,
  item_status VARCHAR(30) DEFAULT 'PENDING',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  FOREIGN KEY (seller_id) REFERENCES sellers(id)
);

CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_seller ON order_items(seller_id);

-- ----------------------------------------------------------------------------
-- 11. PAYMENT TRANSACTION & SHIPMENT DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS payments (
  id VARCHAR(64) PRIMARY KEY,
  order_id VARCHAR(64) NOT NULL,
  payment_method VARCHAR(50) NOT NULL,
  transaction_reference VARCHAR(100) NOT NULL UNIQUE,
  amount DECIMAL(10,2) NOT NULL,
  currency VARCHAR(10) DEFAULT 'USD',
  status VARCHAR(30) NOT NULL,
  gateway_response_json TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id)
);

CREATE TABLE IF NOT EXISTS shipments (
  id VARCHAR(64) PRIMARY KEY,
  order_id VARCHAR(64) NOT NULL,
  carrier VARCHAR(100) NOT NULL,
  tracking_number VARCHAR(100) NOT NULL UNIQUE,
  status VARCHAR(30) DEFAULT 'LABEL_CREATED',
  shipped_at TIMESTAMP,
  delivered_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- ----------------------------------------------------------------------------
-- 12. RETURNS & REFUNDS DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS return_requests (
  id VARCHAR(64) PRIMARY KEY,
  order_id VARCHAR(64) NOT NULL,
  order_item_id VARCHAR(64) NOT NULL,
  user_id VARCHAR(64) NOT NULL,
  reason VARCHAR(100) NOT NULL,
  comments TEXT,
  status VARCHAR(30) DEFAULT 'SUBMITTED',
  refund_amount DECIMAL(10,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (order_id) REFERENCES orders(id),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ----------------------------------------------------------------------------
-- 13. REVIEWS & RATINGS DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS reviews (
  id VARCHAR(64) PRIMARY KEY,
  product_id VARCHAR(64) NOT NULL,
  user_id VARCHAR(64) NOT NULL,
  rating INTEGER NOT NULL CHECK(rating >= 1 AND rating <= 5),
  title VARCHAR(150),
  comment TEXT,
  is_verified_purchase INTEGER DEFAULT 0,
  status VARCHAR(30) DEFAULT 'APPROVED',
  helpful_votes INTEGER DEFAULT 0,
  unhelpful_votes INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);

CREATE TABLE IF NOT EXISTS review_votes (
  review_id VARCHAR(64) NOT NULL,
  user_id VARCHAR(64) NOT NULL,
  vote_type VARCHAR(20) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (review_id, user_id),
  FOREIGN KEY (review_id) REFERENCES reviews(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ----------------------------------------------------------------------------
-- 14. CUSTOMER SUPPORT HELPDESK DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS support_tickets (
  id VARCHAR(64) PRIMARY KEY,
  ticket_number VARCHAR(50) NOT NULL UNIQUE,
  user_id VARCHAR(64) NOT NULL,
  order_id VARCHAR(64),
  subject VARCHAR(200) NOT NULL,
  category VARCHAR(50) NOT NULL DEFAULT 'GENERAL',
  priority VARCHAR(20) DEFAULT 'MEDIUM',
  status VARCHAR(30) DEFAULT 'OPEN',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS support_messages (
  id VARCHAR(64) PRIMARY KEY,
  ticket_id VARCHAR(64) NOT NULL,
  sender_id VARCHAR(64) NOT NULL,
  message TEXT NOT NULL,
  is_internal_note INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (ticket_id) REFERENCES support_tickets(id) ON DELETE CASCADE,
  FOREIGN KEY (sender_id) REFERENCES users(id)
);

-- ----------------------------------------------------------------------------
-- 15. USER ANALYTICS & AUDIT LOGGING DOMAIN
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS recently_viewed (
  user_id VARCHAR(64) NOT NULL,
  product_id VARCHAR(64) NOT NULL,
  viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, product_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS search_history (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64),
  query_text VARCHAR(255) NOT NULL,
  result_count INTEGER DEFAULT 0,
  searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS security_audit_logs (
  id VARCHAR(64) PRIMARY KEY,
  user_id VARCHAR(64),
  action VARCHAR(100) NOT NULL,
  module VARCHAR(50) NOT NULL,
  entity_type VARCHAR(50),
  entity_id VARCHAR(64),
  ip_address VARCHAR(45),
  metadata_json TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_created ON security_audit_logs(created_at);
