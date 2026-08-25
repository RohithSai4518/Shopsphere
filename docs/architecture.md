# ShopSphere Marketplace Platform — System Architecture & Design Blueprint

## Executive Summary
ShopSphere is an independent, production-grade e-commerce marketplace platform engineered with zero copyleft dependencies, robust microservices-ready modularity, and strict adherence to modern security practices.

---

## Architectural Principles

### 1. Separation of Concerns & Modular Service Layer
The backend is structured into decoupled domain services:
- **`authService`** & **`rbacService`**: Identity authentication, JWT issuance, and RBAC authorization middleware.
- **`accountService`**: Profile management, address book, device sessions, and preferences.
- **`catalogService`** & **`bundleService`**: Taxonomy resolution, product filtering, specs grid, and bundle pricing.
- **`cartService`** & **`orderService`**: Server-side cart recalculation, stock reservation, and state-machine order transactions.
- **`inventoryLedgerService`**: Double-entry inventory movement ledger (Receipts, Deductions, Reservations, Releases).
- **`paymentService`**: Abstract payment provider sandbox supporting idempotency and transaction logging.
- **`returnsService`**: Reverse logistics RMA lifecycle and refund authorization.
- **`supportService`**: Helpdesk ticket SLA processing and messaging threads.
- **`auditService`**: Security audit logging for governance and compliance.

### 2. High-Performance Synthetic Database Engine (`db.js`)
To guarantee 100% reliable execution across Windows, Linux, and macOS without requiring native C++ build tools or native SQLite compilation drivers, ShopSphere features a pure JavaScript transactional database layer:
- In-memory state store backed by atomic JSON persistence.
- Complete support for SQLite syntax queries (`prepare`, `run`, `get`, `all`, `transaction`).
- Dynamic store loading for thread-safe concurrent test isolation.

### 3. Comprehensive Security Architecture
- **JWT Authentication**: Short-lived signed JWT bearer tokens paired with refresh tokens.
- **Role-Based Access Control**: Middleware enforcement for `CUSTOMER`, `SELLER`, `SUPPORT`, and `ADMIN` roles.
- **Rate Limiting**: Sliding-window rate limiter protecting against brute-force attacks and DDoS vectors.
- **Security Headers**: Helmet integration (`Content-Security-Policy`, `X-Frame-Options`, `X-Content-Type-Options`).
- **Input Sanitization**: Defense against XSS script injection and SQL parameter tampering.
- **Data Protection**: Strict isolation of environment secrets (`.env`) via `.gitignore` with synthetic placeholders in `.env.example`.

### 4. Premium Responsive Dark Mode Frontend
The React 18 storefront built on Vite delivers a state-of-the-art visual aesthetic:
- Curated color palette (Obsidian, Midnight Glass, Cyberpunk Cyan, Electric Gold).
- Glassmorphism UI components with backdrop blur effects and CSS micro-animations.
- Responsive mobile navigation drawer, interactive search modal, and live cart drawer.
- Zero copyleft components — built entirely using vanilla CSS design tokens and standard React hooks.
