# ShopSphere — Human Developer Technical Review Checklist

This document is reserved for the human developer / senior software architect to perform explicit code review and architectural validation before deploying ShopSphere to staging or production environments.

> [!IMPORTANT]
> The checklist items below MUST remain unchecked until a human developer has independently reviewed and signed off on each component.

---

## 📋 Architectural & Domain Review Checklist

### Architecture
- [ ] Reviewed overall Python/Django project layout, settings, and WSGI/ASGI gateways.

### Authentication
- [ ] Reviewed User model (`apps.accounts.models.User`), password hashing, login forms, session duration, and authentication endpoints.

### RBAC
- [ ] Reviewed Role-Based Access Control matrix (`apps.rbac`), role permissions, and `@role_required` decorator enforcement on views.

### Database
- [ ] Reviewed ORM models across 36 entities, foreign key CASCADE/PROTECT constraints, indexing, and migration files.

### Catalog
- [ ] Reviewed product categories, brands, variants, pricing, discount calculations, and technical specifications.

### Cart
- [ ] Reviewed CartItem model, subtotal calculation context processor, and quantity update validations.

### Orders
- [ ] Reviewed Order state machine transitions, OrderItem linkage, address JSON snapshots, and checkout atomic transactions.

### Inventory
- [ ] Reviewed warehouse locations, stock reservation logic, deduct-on-shipment workflows, and double-entry transaction log.

### Payments
- [ ] Reviewed payment gateway abstraction, transaction reference generation, refund handling, and PCI compliance (zero card data stored).

### Returns
- [ ] Reviewed RMA return request submission, restocking fee calculations, inventory credit restock, and refund integration.

### Seller Platform
- [ ] Reviewed merchant seller profile approval, commission rate calculations, merchant dashboard, and order item fulfillment queue.

### Admin Platform
- [ ] Reviewed platform governance dashboard, seller approval workflow, and security audit log viewer.

### Security
- [ ] Reviewed Django deployment security settings (`check --deploy`), CSRF protection, session cookie flags, and secret environment isolation (`.env`).

### Tests
- [ ] Reviewed unit and integration test coverage across models, services, and storefront views.
