# ShopSphere Automated Testing Strategy

## 1. Testing Pyramid Overview

ShopSphere maintains a comprehensive testing strategy covering unit tests, integration tests, API route tests, and end-to-end user flows.

```
       / \
      /   \      E2E User Flow Tests
     /     \     (Cart, Checkout, Seller Portal)
    /-------\
   /         \   API Integration Tests
  /           \  (Endpoints, Auth RBAC, Order State)
 /-------------\
/               \ Unit Tests
----------------- (Calculations, Validators, State Machines)
```

---

## 2. Test Suite Organization

- **Unit Tests**: Test isolated utility functions, price calculation engines, stock allocation rules, coupon validation, and Zod schemas.
- **Integration Tests**: Test repository query operations against SQLite/PostgreSQL, transactional rollback, and inventory locking.
- **API Tests**: Supertest HTTP execution against Express REST endpoints for status codes, headers, and payload structures.
- **Security Tests**: Validate unauthenticated route blocks, expired token rejections, role enforcement (e.g. non-admin access to `/api/v1/admin`), and XSS sanitization.

---

## 3. Running Test Suites

```bash
# Run all automated tests
npm test

# Run unit tests only
npm run test:unit

# Run API integration tests
npm run test:api
```
