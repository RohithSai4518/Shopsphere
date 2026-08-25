# ShopSphere Architectural Decision Records (ADR)

## ADR 001: Strict MIT/BSD/ISC Open-Source Licensing Policy

### Context & Problem
To ensure ShopSphere is 100% commercially safe, copyleft-free, and enterprise compliant, all dependencies must be audited for license compliance. Many popular packages use GPL, AGPL, LGPL, or Apache-2.0 licenses.

### Decision
We strictly enforce an MIT/BSD/ISC license policy. All introduced packages must be audited and registered in `docs/dependency-license-register.md`. Any package with GPL, AGPL, LGPL, or Apache-2.0 licenses is strictly prohibited.

---

## ADR 002: Modular Decoupled Monorepo Structure

### Context & Problem
The platform requires Customer, Seller, and Admin interfaces alongside a comprehensive multi-tenant API backend targetting 50,000+ LOC.

### Decision
We adopt a workspace monorepo layout separating `server/` (Node.js REST API), `client/` (React + Vite Storefront & Dashboards), `docs/`, `scripts/`, and `tests/`.

---

## ADR 003: Server-Side Financial and Stock Validation

### Context & Problem
E-commerce applications are susceptible to price manipulation and stock overselling if logic relies on client payloads.

### Decision
All pricing calculations, tax calculations, discounts, coupons, and stock availability checks are strictly executed and validated on the backend within ACID database transactions.
