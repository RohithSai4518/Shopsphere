# ShopSphere REST API Documentation Specification

## 1. Global API Standards

- **Base URL**: `/api/v1`
- **Protocol**: HTTPS
- **Content-Type**: `application/json`
- **Authentication**: `Authorization: Bearer <JWT_ACCESS_TOKEN>` or Secure HTTP-Only Cookie.

---

## 2. Response Standard Envelopes

### Success Envelope (HTTP 200 / 201)
```json
{
  "success": true,
  "data": {},
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "timestamp": "2026-08-25T10:00:00.000Z"
  }
}
```

### Error Envelope (HTTP 4xx / 5xx)
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE_IDENTIFIER",
    "message": "Human-readable safe error message",
    "details": []
  },
  "timestamp": "2026-08-25T10:00:00.000Z"
}
```

---

## 3. Core API Endpoints Overview

### Auth Domain (`/api/v1/auth`)
- `POST /register`: Register a new customer or seller account.
- `POST /login`: Authenticate and obtain JWT access token.
- `POST /refresh-token`: Rotate refresh token and issue new access token.
- `POST /logout`: Revoke active session tokens.
- `GET /me`: Fetch authenticated user profile and roles.

### Catalog Domain (`/api/v1/products` & `/api/v1/categories`)
- `GET /products`: List products with pagination, search keywords, category filtering, and sorting.
- `GET /products/:id`: Fetch detailed product attributes, variants, reviews, and stock.
- `POST /products`: (Seller/Admin) Create new product with variants.
- `PUT /products/:id`: (Seller/Admin) Update product details.
- `GET /categories`: Browse hierarchical category tree.

### Cart & Wishlist Domain (`/api/v1/cart`)
- `GET /cart`: Fetch active cart items, subtotal, shipping estimate, and tax.
- `POST /cart/items`: Add item variant to cart.
- `PUT /cart/items/:id`: Update item quantity.
- `DELETE /cart/items/:id`: Remove item from cart.

### Order Domain (`/api/v1/orders`)
- `POST /orders`: Place order (validates stock, applies coupon, locks inventory, creates order record).
- `GET /orders`: List user orders.
- `GET /orders/:id`: Get order breakdown, tracking history, and items.
- `POST /orders/:id/cancel`: Cancel pending/processing order.

### Seller Domain (`/api/v1/seller`)
- `GET /seller/dashboard`: Metrics on sales, revenue, active inventory, pending orders.
- `GET /seller/orders`: List orders containing seller's items.
- `POST /seller/orders/:id/fulfill`: Update shipping status and tracking code.

### Admin Domain (`/api/v1/admin`)
- `GET /admin/analytics`: Platform-wide financial and user analytics.
- `GET /admin/sellers/pending`: List sellers awaiting registration approval.
- `POST /admin/sellers/:id/approve`: Approve seller registration.
- `POST /admin/coupons`: Create system promotional coupon codes.
- `GET /admin/audit-logs`: View system audit trail logs.
