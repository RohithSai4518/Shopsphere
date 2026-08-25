# ShopSphere Marketplace Platform — REST API Specification

## Overview
ShopSphere exposes a production-grade, highly scalable RESTful API built with Express.js and Node.js.
All endpoints enforce strict input validation, security rate-limiting, Helmet security headers, CORS policies, XSS sanitization, and structured JSON responses with standard success metadata and error contracts.

---

## Base API Endpoint URL
```
HTTP Base: http://localhost:5000/api/v1
```

---

## Standard Response Schema

### Success Response Contract (`200 OK`, `201 Created`)
```json
{
  "success": true,
  "data": { ... },
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "timestamp": "2026-08-25T05:00:00.000Z"
  }
}
```

### Error Response Contract (`400`, `401`, `403`, `404`, `429`, `500`)
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email address format.",
    "details": []
  },
  "timestamp": "2026-08-25T05:00:00.000Z"
}
```

---

## Domain Endpoint Catalog

### 1. Authentication & Security Services (`/api/v1/auth`)
* `POST /api/v1/auth/register` — Register a new platform account (Customer or Seller).
* `POST /api/v1/auth/login` — Authenticate credentials and issue JWT bearer token & refresh token.
* `POST /api/v1/auth/refresh` — Refresh access token using valid refresh token.
* `POST /api/v1/auth/logout` — Invalidate user active session token.

### 2. Customer Account & Address Book (`/api/v1/account`)
* `PUT /api/v1/account/profile` — Update user profile details (First Name, Last Name, Phone).
* `PUT /api/v1/account/password` — Secure password update with current password validation.
* `GET /api/v1/account/addresses` — Fetch user saved address book list.
* `POST /api/v1/account/addresses` — Add new shipping or billing address.
* `DELETE /api/v1/account/addresses/:id` — Delete address entry.
* `GET /api/v1/account/sessions` — View active device login sessions.
* `DELETE /api/v1/account/sessions/:id` — Revoke device session.
* `GET /api/v1/account/preferences` — Get notification & theme preferences.
* `PUT /api/v1/account/preferences` — Update notification & currency settings.
* `GET /api/v1/account/recently-viewed` — Fetch recently viewed product history.

### 3. Product Catalog & Taxonomy (`/api/v1`)
* `GET /api/v1/categories` — Get active product category hierarchy.
* `GET /api/v1/products` — Advanced search with keyword, category, price range, brand, sorting, and pagination.
* `GET /api/v1/products/:slug` — Get comprehensive product details with variants, specs, and primary images.
* `GET /api/v1/products/:id/reviews` — Fetch approved customer reviews and average rating score.
* `POST /api/v1/products/:id/reviews` — Submit verified purchase product review.
* `POST /api/v1/reviews/:id/vote` — Upvote or downvote product review helpfulness.

### 4. Wishlists & Price Alerts (`/api/v1/wishlist`)
* `GET /api/v1/wishlist` — Fetch user wishlists and saved items.
* `POST /api/v1/wishlist` — Create custom named wishlist.
* `POST /api/v1/wishlist/:wishlistId/items` — Add product item to wishlist.
* `DELETE /api/v1/wishlist/items/:itemId` — Remove item from wishlist.
* `POST /api/v1/wishlist/price-alerts` — Create target price drop alert.

### 5. Shopping Cart (`/api/v1/cart`)
* `GET /api/v1/cart` — Fetch server-side cart with price calculations, discounts, and stock limits.
* `POST /api/v1/cart/items` — Add variant item to cart with quantity validation.
* `PUT /api/v1/cart/items/:id` — Update cart item quantity.
* `DELETE /api/v1/cart/items/:id` — Remove item from cart.
* `DELETE /api/v1/cart` — Clear entire cart.

### 6. Multi-Step Checkout & Orders (`/api/v1/orders`)
* `POST /api/v1/orders` — Create order transaction with coupon validation and sandbox payment authorization.
* `GET /api/v1/orders` — Fetch customer order history.
* `GET /api/v1/orders/:id` — Fetch detailed order timeline, items, shipment tracking, and payment status.

### 7. Returns & Refunds (`/api/v1/returns`)
* `POST /api/v1/returns` — Submit return request for eligible order item.
* `GET /api/v1/returns` — Fetch customer return request history.
* `POST /api/v1/returns/:id/approve` — Merchant/Admin approval or rejection of return request.

### 8. Customer Support Helpdesk (`/api/v1/support`)
* `POST /api/v1/support/tickets` — Create customer support helpdesk ticket.
* `GET /api/v1/support/tickets` — List customer support tickets.
* `GET /api/v1/support/tickets/:id` — Get ticket conversation thread and SLA priority.
* `POST /api/v1/support/tickets/:id/messages` — Send reply message or internal staff note.
* `GET /api/v1/support/tickets/admin/all` — Support staff ticket queue management.

### 9. Merchant & Seller Portal (`/api/v1/seller`)
* `GET /api/v1/seller/dashboard` — Merchant metrics (Total Sales, Revenue, Pending Orders, Low Stock Alerts).
* `GET /api/v1/seller/orders` — Merchant order fulfillment queue.
* `POST /api/v1/seller/orders/fulfill` — Fulfill order item with carrier and tracking number.
* `POST /api/v1/seller/products` — Create new merchant product listing.

### 10. Platform Administration & Security Analytics (`/api/v1/admin`, `/api/v1/rbac`, `/api/v1/analytics`)
* `GET /api/v1/admin/analytics` — Platform aggregated metrics (Total Revenue, Active Users, Commissions, Orders).
* `GET /api/v1/admin/sellers` — View pending merchant registration requests.
* `POST /api/v1/admin/sellers/:id/approve` — Approve or reject seller merchant application.
* `GET /api/v1/rbac/roles` — View role definitions.
* `GET /api/v1/rbac/permissions` — View granular permission codes.
* `POST /api/v1/rbac/user-roles` — Assign RBAC roles to platform users.
* `GET /api/v1/analytics/audit-logs` — Security audit trail log viewer.
