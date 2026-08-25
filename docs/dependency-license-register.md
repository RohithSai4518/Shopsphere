# ShopSphere Dependency License Register

## 1. Licensing Policy Overview

This repository enforces a strict open-source licensing policy to maintain full independence, commercial safety, and copyleft/restriction compliance.

### Approved Licenses
* **MIT**
* **BSD-2-Clause**
* **BSD-3-Clause**
* **ISC**
* **CC0-1.0** / Public Domain

### Prohibited Licenses
* **GPL (v1, v2, v3)**
* **AGPL (v1, v2, v3)**
* **LGPL (v1, v2, v3)**
* **Apache-1.0 / Apache-2.0**
* **SSPL / Commons Clause / Non-Commercial Licenses**

---

## 2. Dependency Audit Register

| Package Name | Version | License | Direct / Transitive | Purpose / Function | Approval Status | Audit Notes / Reason |
|---|---|---|---|---|---|---|
| `express` | `^4.19.0` | MIT | Direct | Backend REST web server framework | ✅ APPROVED | Permissive MIT license |
| `bcryptjs` | `^2.4.3` | MIT | Direct | Pure JavaScript password hashing (bcrypt) | ✅ APPROVED | Permissive MIT license |
| `jsonwebtoken` | `^9.0.2` | MIT | Direct | JWT sign & verify for session tokens | ✅ APPROVED | Permissive MIT license |
| `better-sqlite3` | `^9.4.0` | MIT | Direct | Fast, synchronous SQLite DB driver for dev/testing | ✅ APPROVED | Permissive MIT license |
| `zod` | `^3.22.4` | MIT | Direct | Schema validation for API payloads | ✅ APPROVED | Permissive MIT license |
| `cors` | `^2.8.5` | MIT | Direct | Express cross-origin resource sharing middleware | ✅ APPROVED | Permissive MIT license |
| `helmet` | `^7.1.0` | MIT | Direct | Express HTTP security headers | ✅ APPROVED | Permissive MIT license |

---

## 3. License Audit Verification Script

All project dependencies are programmatically scanned prior to deployment via `scripts/license-audit.js`.
Any package containing a GPL, AGPL, LGPL, or Apache license will instantly break the build pipeline.
