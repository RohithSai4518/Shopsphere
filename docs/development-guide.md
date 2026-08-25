# ShopSphere Development & Engineering Guide

## 1. Developer Onboarding

### Environment Prerequisites
- Node.js v18+ LTS
- npm v9+

### Setup Commands
```bash
# 1. Clone repository
git clone <repository_url>
cd Amazon_Clone

# 2. Configure Environment
cp .env.example .env

# 3. License Audit Check
npm run license:audit

# 4. Install Dependencies & Launch Dev Server
npm install
npm run dev
```

---

## 2. Coding Standards & Conventions

1. **JavaScript Standard**: ES2022+ features (Async/Await, Arrow Functions, Modules).
2. **File Naming**:
   - Backend controllers/services: camelCase (`productController.js`, `orderService.js`).
   - React components: PascalCase (`ProductCard.jsx`, `CheckoutWizard.jsx`).
   - Style sheets: CSS Modules (`ProductCard.module.css`).
3. **Layer Separation**: Controllers handles HTTP only; Services contain all domain business rules; Models handle DB queries only.
4. **Error Handling**: Use explicit custom `AppError` exceptions with standard HTTP status codes. Never swallow errors or return silent fallbacks.

---

## 3. Human Review Points

For every pull request and feature implementation:
1. Verify business purpose and domain architecture match specifications.
2. Ensure input schemas use `Zod` validation.
3. Verify zero GPL/Apache-2.0 dependencies were introduced.
4. Confirm test coverage exists for success and edge failure cases.
