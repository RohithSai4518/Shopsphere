# ShopSphere Testing Guide

## Test Architecture
ShopSphere includes a comprehensive Django unit and integration test suite located in `tests/`.

---

## Executing Tests

### Run All Tests
```bash
python manage.py test tests
```

### Test Module Breakdown & Coverage

| Test Module | Domain / App Covered | Key Test Scenarios |
| :--- | :--- | :--- |
| `tests/test_accounts.py` | `apps.accounts` | User creation, password hashing, default address flag auto-reset |
| `tests/test_catalog.py` | `apps.catalog` | Effective price calculation, discount percentage, variant price override |
| `tests/test_cart.py` | `apps.cart` | CartItem subtotal calculation, quantity multipliers |
| `tests/test_orders.py` | `apps.orders` | Order creation, line item linkage, totals validation |
| `tests/test_services.py` | `apps.*.services` | OrderService checkout, InventoryService restock, PromotionService coupon validation, Seller analytics |
| `tests/test_rbac.py` | `apps.rbac` | `@role_required` decorator access allowed/denied enforcement |
| `tests/test_sellers.py` | `apps.sellers` | Seller merchant profile creation & status |
| `tests/test_promotions.py` | `apps.promotions` | Coupon percentage calculation, minimum order subtotal enforcement |
| `tests/test_returns.py` | `apps.returns` | ReturnRequest creation and status tracking |
| `tests/test_notifications.py` | `apps.notifications` | Notification dispatch & mark-all-read |
| `tests/test_analytics.py` | `apps.analytics` | RecentlyViewed recording, search query logging |
| `tests/test_payments.py` | `apps.payments` | Payment sandbox authorization & refund handling |
| `tests/test_catalog_services.py` | `apps.catalog.services` | Product search query filters, price filters, bundle savings calculations |
| `tests/test_views.py` | `apps.catalog.views` | Homepage HTTP status 200, product list rendering, product detail rendering |
