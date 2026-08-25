# ShopSphere Database Schema Documentation

## Database Overview
ShopSphere uses a relational database architecture (SQLite for portable development, PostgreSQL for production) containing **36 normalized entities** in Third Normal Form (3NF).

---

## Entity Relationship Matrix (16 Domain Apps / 36 Models)

### 1. Accounts & Authentication (`apps/accounts/models.py`)
- `User`: Custom user model inheriting Django `AbstractUser`. Primary Key: `usr_<uuid>`. Fields: `email` (unique), `phone`, `role` (CUSTOMER, SELLER, SUPPORT, ADMIN), `status`, `is_verified`.
- `Address`: Recipient addresses. Foreign Key: `User`. Types: SHIPPING, BILLING. Includes automatic `is_default` single-active flag reset.
- `UserSession`: Active login sessions tracking IP address, user agent, token hash, and expiry.
- `LoginHistory`: Audit log of user login attempts.
- `UserPreference`: One-to-one preferences for notifications, theme, and currency.

### 2. Role-Based Access Control (`apps/rbac/models.py`)
- `Role`: Security roles (ADMIN, SELLER, CUSTOMER, SUPPORT).
- `Permission`: Granular permission codes (e.g. `manage_catalog`, `manage_orders`).
- `RolePermission`: Many-to-many junction connecting `Role` to `Permission`.
- `UserRole`: Many-to-many junction connecting `User` to `Role`.

### 3. Merchant Sellers (`apps/sellers/models.py`)
- `Seller`: One-to-one profile with `User`. Stores `business_name`, `business_email`, `tax_id`, `commission_rate` (default 8.50%), `rating_avg`, and `status` (PENDING, APPROVED, SUSPENDED).

### 4. Catalog & Products (`apps/catalog/models.py`)
- `Category`: Hierarchical taxonomy (self-referencing `parent` foreign key), name, slug, icon URL.
- `Brand`: Manufacturer brand details.
- `Product`: Product listing. Foreign keys: `Seller`, `Category`, `Brand`. Stores `base_price`, `discount_percent`, `tax_rate`, `status` (DRAFT, PUBLISHED, ARCHIVED). Properties: `effective_price`, `primary_image`.
- `ProductVariant`: SKU variants (e.g. color/RAM). Foreign key: `Product`. Stores `sku`, `price_override`, `attributes_json`.
- `ProductSpecification`: Technical specifications (`spec_key`, `spec_value`, `display_group`).
- `ProductImage`: Product image URLs (`is_primary`, `display_order`).
- `ProductBundle`: Curated product package with bundle discount percentage.
- `BundleItem`: Junction connecting `ProductBundle` to `Product`.

### 5. Warehouse & Inventory (`apps/inventory/models.py`)
- `WarehouseLocation`: Physical warehouse facilities (`code`, `address`, `city`, `state`, `country`).
- `Inventory`: One-to-one with `ProductVariant`. Stores `quantity_on_hand`, `quantity_reserved`, `reorder_threshold`. Property: `quantity_available`.
- `InventoryTransaction`: Double-entry stock transaction ledger (`transaction_type`: RECEIPT, DEDUCTION, RESERVATION, RELEASE, RETURN).

### 6. Cart & Wishlist (`apps/cart/models.py`, `apps/wishlist/models.py`)
- `CartItem`: Unique user-variant cart entry. Stores `quantity`. Properties: `unit_price`, `effective_unit_price`, `subtotal`.
- `Wishlist`: Saved product list.
- `WishlistItem`: Junction connecting `Wishlist` to `Product`.
- `PriceAlert`: Price threshold drop notifications for products.

### 7. Promotions (`apps/promotions/models.py`)
- `Coupon`: Promo codes (`discount_type`: PERCENTAGE, FIXED), `discount_value`, `min_order_subtotal`, date validity windows.
- `PromotionalCampaign`: Promotional marketing campaign banners and discounts.

### 8. Orders & Payments (`apps/orders/models.py`, `apps/payments/models.py`)
- `Order`: Customer order header. Foreign keys: `User`, `Coupon`. Stores `order_number`, `status` (PENDING, CONFIRMED, PROCESSING, SHIPPED, OUT_FOR_DELIVERY, DELIVERED, CANCELLED, RETURNED), `subtotal`, `tax_amount`, `shipping_amount`, `total_amount`, address JSON snapshots.
- `OrderItem`: Line item. Foreign keys: `Order`, `ProductVariant`, `Seller`. Stores `unit_price`, `quantity`, `total_price`, `item_status`.
- `Shipment`: Shipping package details (`carrier`, `tracking_number`, `status`, dates).
- `Payment`: Sandbox payment transaction reference (`payment_method`, `transaction_reference`, `amount`, `status`, gateway response JSON).

### 9. Returns, Reviews, Support, Analytics, Audit (`apps/*/models.py`)
- `ReturnRequest`: RMA return request (`reason`, `comments`, `status`, `refund_amount`).
- `Review`: Verified purchase product rating (1-5 stars) and review comment.
- `ReviewVote`: Helpful / unhelpful review voting.
- `SupportTicket`: SLA customer helpdesk ticket (`ticket_number`, `subject`, `category`, `priority`, `status`).
- `SupportMessage`: Messaging thread for support tickets.
- `Notification`: In-app notification alerts (`notification_type`, `is_read`).
- `RecentlyViewed`: Collaborative product view history.
- `SearchHistory`: Search query analytics and result counts.
- `SecurityAuditLog`: Platform administrative audit log (`action`, `module`, `entity_type`, `entity_id`, `ip_address`, `metadata_json`).
