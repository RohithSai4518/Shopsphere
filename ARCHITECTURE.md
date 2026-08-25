# ShopSphere Architecture & Technical Design Specification

## Overview
ShopSphere is an enterprise-grade, Amazon-inspired e-commerce marketplace platform built using a **Python-First Full-Stack Architecture**. It completely replaces prior Node.js/React implementations with a robust Python/Django backend, Django ORM, server-rendered Django Templates, Django Forms, and custom domain service layers.

---

## 16 Domain Applications Structure

1. `apps.accounts`: Custom User authentication, address book, login audit trail, user preferences.
2. `apps.rbac`: Role-Based Access Control (ADMIN, SELLER, CUSTOMER, SUPPORT), permissions, `@role_required` decorators.
3. `apps.sellers`: Merchant profiles, commission rate tracking, seller rating, fulfillment queue.
4. `apps.catalog`: Hierarchical categories, brands, products, product variants, specifications, image gallery, bundles.
5. `apps.inventory`: Warehouse locations, stock ledger, real-time stock reservations, inventory transaction log.
6. `apps.cart`: Shopping cart items, live subtotal context processor, tax calculations.
7. `apps.wishlist`: Saved product lists, price drop alerts.
8. `apps.promotions`: Coupon code validation, fixed/percentage discounts, campaign banners.
9. `apps.orders`: Order state machine, line items, shipment creation, tracking numbers.
10. `apps.payments`: Sandbox payment authorization, transaction reference generation, refund processing.
11. `apps.returns`: RMA return request submission, reason code tracking, refund status.
12. `apps.reviews`: Customer product reviews, verified purchase verification, helpful votes.
13. `apps.support`: SLA helpdesk tickets, multi-party messaging thread, ticket escalation.
14. `apps.notifications`: In-app system alerts, order updates.
15. `apps.analytics`: Search history logging, recently viewed items collaborative filtering.
16. `apps.audit`: Security event logs, IP tracking, administrative audit trail.

---

## Database ERD & Relational Schema (36 Entities)

ShopSphere's database schema maps to 36 relational models in Third Normal Form (3NF), including:
- `accounts_user`, `accounts_address`, `accounts_usersession`, `accounts_loginhistory`, `accounts_userpreference`
- `rbac_role`, `rbac_permission`, `rbac_rolepermission`, `rbac_userrole`
- `sellers_seller`
- `catalog_category`, `catalog_brand`, `catalog_product`, `catalog_productvariant`, `catalog_productspecification`, `catalog_productimage`, `catalog_productbundle`, `catalog_bundleitem`
- `inventory_warehouselocation`, `inventory_inventory`, `inventory_inventorytransaction`
- `cart_cartitem`
- `wishlist_wishlist`, `wishlist_wishlistitem`, `wishlist_pricealert`
- `promotions_coupon`, `promotions_promotionalcampaign`
- `orders_order`, `orders_orderitem`, `orders_shipment`
- `payments_payment`
- `returns_returnrequest`
- `reviews_review`, `reviews_reviewvote`
- `support_supportticket`, `support_supportmessage`
- `notifications_notification`
- `analytics_recentlyviewed`, `analytics_searchhistory`
- `audit_securityauditlog`

---

## Human Developer Review Notes & Security
- **Strict License Policy**: 100% compliance with BSD-3-Clause, MIT, ISC, and PSF licenses.
- **Zero Copyleft**: Guaranteed zero GPL/AGPL/LGPL/Apache-2.0 dependencies.
- **Secrets Isolation**: All sensitive settings loaded from `.env`. Zero secrets committed to git.
- **Transaction Safety**: Atomic database transactions wrapped via `@transaction.atomic` for checkout and inventory reservation.
