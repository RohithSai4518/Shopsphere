# ShopSphere — Dependency License Register & Compliance Audit Report

## Strict Licensing Policy Statement
ShopSphere enforces a strict permissive-only open-source dependency policy.
- **PROHIBITED LICENSES**: GNU General Public License (GPL, GPLv2, GPLv3), GNU Affero General Public License (AGPL), GNU Lesser General Public License (LGPL), Apache License 2.0 (Apache-2.0).
- **PERMITTED LICENSES**: MIT License, BSD 2-Clause, BSD 3-Clause, ISC License, CC0 1.0 Universal.

---

## Dependency Inventory & License Verification

| Package Name | Category | Version | License | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| `express` | Backend Core Framework | `^4.19.2` | **MIT** | ✅ Verified Compliant |
| `bcryptjs` | Password Hashing | `^2.4.3` | **MIT** | ✅ Verified Compliant |
| `jsonwebtoken` | JWT Auth Tokens | `^9.0.2` | **MIT** | ✅ Verified Compliant |
| `cors` | Cross-Origin Middleware | `^2.8.5` | **MIT** | ✅ Verified Compliant |
| `helmet` | Security Headers | `^7.1.0` | **MIT** | ✅ Verified Compliant |
| `zod` | Schema Validation | `^3.23.8` | **MIT** | ✅ Verified Compliant |
| `react` | Frontend UI Library | `^18.3.1` | **MIT** | ✅ Verified Compliant |
| `react-dom` | React Web Renderer | `^18.3.1` | **MIT** | ✅ Verified Compliant |
| `react-router-dom` | SPA Router | `^6.26.1` | **MIT** | ✅ Verified Compliant |
| `vite` | Frontend Build Tool | `^5.4.2` | **MIT** | ✅ Verified Compliant |
| `@vitejs/plugin-react` | Vite React Plugin | `^4.3.1` | **MIT** | ✅ Verified Compliant |

---

## Automated License Compliance Verification
License compliance is automatically validated via the customized audit tool `scripts/license-audit.js`:
```bash
node scripts/license-audit.js
```
Audit Result: **100% License Compliance (0 Prohibited Licenses Found)**.
