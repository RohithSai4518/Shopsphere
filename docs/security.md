# ShopSphere Security & Compliance Guide

## Security Architecture Overview
ShopSphere implements security controls at every application layer:

1. **Authentication & Password Hardening**:
   - Django `PBKDF2` algorithm with SHA-256 password hashing.
   - Built-in password strength validators (`MinimumLengthValidator`, `CommonPasswordValidator`, `NumericPasswordValidator`).
   - Session duration limit (7 days default) with HTTP-only session cookies.

2. **Authorization & RBAC Enforcement**:
   - Server-side Python decorator `@role_required(*roles)` enforced on all protected views.
   - 4-Tier privilege hierarchy: `CUSTOMER`, `SELLER`, `SUPPORT`, `ADMIN`.
   - UI navigation hiding is supplemented by strict Python view authorization.

3. **Database Security & Secrets Management**:
   - Zero hardcoded production secrets in source control.
   - Environment settings loaded dynamically via `python-dotenv` from `.env`.
   - Parameterized SQL queries executed strictly via Django ORM preventing SQL injection attacks.

4. **CSRF & XSS Protection**:
   - `CsrfViewMiddleware` active across all HTTP POST forms.
   - Django template auto-escaping enabled by default against Cross-Site Scripting (XSS).

5. **PCI-DSS Compliance (Payment Gateway Abstraction)**:
   - Zero raw credit card numbers, CVVs, or PINs stored in the database.
   - Abstract sandbox payment gateway generates synthetic transaction reference identifiers (`TXN-SANDBOX-*`).

---

## Deployment Security Checklist (`python manage.py check --deploy`)

When deploying to production over HTTPS, enable the following settings in `.env` / `settings.py`:
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
DEBUG = False
```
