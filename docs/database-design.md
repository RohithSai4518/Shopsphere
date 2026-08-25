# ShopSphere Relational Database Design Specification

## 1. Relational Schema Architecture

ShopSphere uses a fully normalized (3NF) relational schema designed for transactional integrity, strict data types, foreign key constraints, and index optimization.

---

## 2. Table Specifications & Schema Definitions

### 2.1 User & Identity Tables
- **`users`**: Core credentials and user profile info.
  - `id`: UUID / Auto-Increment INT (Primary Key)
  - `email`: VARCHAR(255) UNIQUE NOT NULL
  - `password_hash`: VARCHAR(255) NOT NULL
  - `first_name`: VARCHAR(100) NOT NULL
  - `last_name`: VARCHAR(100) NOT NULL
  - `role`: VARCHAR(20) CHECK (role IN ('CUSTOMER', 'SELLER', 'ADMIN', 'SUPPORT'))
  - `is_verified`: BOOLEAN DEFAULT FALSE
  - `status`: VARCHAR(20) DEFAULT 'ACTIVE'
  - `created_at`: TIMESTAMP
  - `updated_at`: TIMESTAMP

- **`sellers`**: Seller entity profile linked to `users`.
  - `id`: UUID / INT (Primary Key)
  - `user_id`: FK -> `users.id` UNIQUE
  - `business_name`: VARCHAR(255) NOT NULL
  - `tax_id`: VARCHAR(100)
  - `status`: VARCHAR(20) DEFAULT 'PENDING' CHECK (status IN ('PENDING', 'APPROVED', 'REJECTED', 'SUSPENDED'))
  - `commission_rate`: DECIMAL(5,2) DEFAULT 10.00
  - `created_at`: TIMESTAMP

- **`addresses`**: User shipping/billing addresses.
  - `id`: Primary Key
  - `user_id`: FK -> `users.id`
  - `address_type`: VARCHAR(20) CHECK (address_type IN ('SHIPPING', 'BILLING'))
  - `full_name`: VARCHAR(255)
  - `street_address_1`: VARCHAR(255) NOT NULL
  - `street_address_2`: VARCHAR(255)
  - `city`: VARCHAR(100) NOT NULL
  - `state`: VARCHAR(100) NOT NULL
  - `postal_code`: VARCHAR(20) NOT NULL
  - `country`: VARCHAR(100) NOT NULL
  - `is_default`: BOOLEAN DEFAULT FALSE

---

### 2.2 Taxonomy & Catalog Tables
- **`categories`**: Hierarchical category tree.
  - `id`: Primary Key
  - `parent_id`: FK -> `categories.id` (NULLABLE for top-level)
  - `name`: VARCHAR(100) NOT NULL
  - `slug`: VARCHAR(100) UNIQUE NOT NULL
  - `description`: TEXT
  - `is_active`: BOOLEAN DEFAULT TRUE

- **`products`**: Parent product metadata.
  - `id`: Primary Key
  - `seller_id`: FK -> `sellers.id`
  - `category_id`: FK -> `categories.id`
  - `name`: VARCHAR(255) NOT NULL
  - `slug`: VARCHAR(255) UNIQUE NOT NULL
  - `brand`: VARCHAR(100)
  - `description`: TEXT
  - `base_price`: DECIMAL(10,2) NOT NULL
  - `discount_percent`: DECIMAL(5,2) DEFAULT 0.00
  - `tax_rate`: DECIMAL(5,2) DEFAULT 0.00
  - `status`: VARCHAR(20) DEFAULT 'DRAFT'
  - `created_at`: TIMESTAMP

- **`product_variants`**: Specific SKUs (size, color, specifications).
  - `id`: Primary Key
  - `product_id`: FK -> `products.id`
  - `sku`: VARCHAR(100) UNIQUE NOT NULL
  - `variant_name`: VARCHAR(255) NOT NULL
  - `price_override`: DECIMAL(10,2) (NULLABLE)
  - `attributes_json`: TEXT / JSONB
  - `weight_kg`: DECIMAL(8,3)
  - `is_default`: BOOLEAN DEFAULT FALSE

- **`inventory`**: Real-time stock counts.
  - `id`: Primary Key
  - `variant_id`: FK -> `product_variants.id` UNIQUE
  - `quantity_on_hand`: INT NOT NULL DEFAULT 0
  - `quantity_reserved`: INT NOT NULL DEFAULT 0
  - `updated_at`: TIMESTAMP

---

### 2.3 Cart, Order & Checkout Tables
- **`cart_items`**: Persistent shopping cart.
  - `id`: Primary Key
  - `user_id`: FK -> `users.id`
  - `variant_id`: FK -> `product_variants.id`
  - `quantity`: INT NOT NULL CHECK (quantity > 0)
  - `created_at`: TIMESTAMP

- **`orders`**: Transactional order records.
  - `id`: Primary Key
  - `order_number`: VARCHAR(50) UNIQUE NOT NULL
  - `user_id`: FK -> `users.id`
  - `status`: VARCHAR(30) CHECK (status IN ('PENDING', 'CONFIRMED', 'PROCESSING', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURN_REQUESTED', 'REFUNDED'))
  - `subtotal`: DECIMAL(10,2) NOT NULL
  - `tax_amount`: DECIMAL(10,2) NOT NULL
  - `shipping_amount`: DECIMAL(10,2) NOT NULL
  - `discount_amount`: DECIMAL(10,2) DEFAULT 0.00
  - `total_amount`: DECIMAL(10,2) NOT NULL
  - `coupon_id`: FK -> `coupons.id` (NULLABLE)
  - `shipping_address_json`: TEXT / JSONB NOT NULL
  - `billing_address_json`: TEXT / JSONB NOT NULL
  - `created_at`: TIMESTAMP

- **`order_items`**: Snapshot of purchased item variants.
  - `id`: Primary Key
  - `order_id`: FK -> `orders.id`
  - `variant_id`: FK -> `product_variants.id`
  - `seller_id`: FK -> `sellers.id`
  - `unit_price`: DECIMAL(10,2) NOT NULL
  - `quantity`: INT NOT NULL
  - `total_price`: DECIMAL(10,2) NOT NULL
  - `item_status`: VARCHAR(30) DEFAULT 'PENDING'

---

### 2.4 Governance, Reviews & Audit
- **`coupons`**: Discount promotions.
  - `id`: Primary Key
  - `code`: VARCHAR(50) UNIQUE NOT NULL
  - `discount_type`: VARCHAR(20) CHECK (discount_type IN ('PERCENTAGE', 'FIXED'))
  - `discount_value`: DECIMAL(10,2) NOT NULL
  - `min_order_subtotal`: DECIMAL(10,2) DEFAULT 0.00
  - `usage_limit`: INT DEFAULT NULL
  - `starts_at`: TIMESTAMP
  - `expires_at`: TIMESTAMP
  - `is_active`: BOOLEAN DEFAULT TRUE

- **`reviews`**: Ratings & Moderated User Reviews.
  - `id`: Primary Key
  - `product_id`: FK -> `products.id`
  - `user_id`: FK -> `users.id`
  - `rating`: INT CHECK (rating BETWEEN 1 AND 5)
  - `title`: VARCHAR(255)
  - `comment`: TEXT
  - `is_verified_purchase`: BOOLEAN DEFAULT FALSE
  - `status`: VARCHAR(20) DEFAULT 'APPROVED'

- **`audit_logs`**: System event tracking.
  - `id`: Primary Key
  - `user_id`: FK -> `users.id` (NULLABLE)
  - `action`: VARCHAR(100) NOT NULL
  - `entity_type`: VARCHAR(50) NOT NULL
  - `entity_id`: VARCHAR(100)
  - `ip_address`: VARCHAR(45)
  - `created_at`: TIMESTAMP
