# ShopSphere Deployment & Production Operations Guide

## 1. Containerization Architecture

ShopSphere applications are containerized using standard lightweight Linux base images (Alpine / Node LTS).

- **Backend Service Dockerfile**: Multi-stage build compiling dependencies and running Node.js production web server.
- **Frontend App Dockerfile**: Multi-stage build bundling React app with Vite and serving via custom NGINX / Caddy static web server.
- **Docker Compose**: Production-like local orchestration linking Node Backend, PostgreSQL Database, and NGINX Reverse Proxy.

---

## 2. Production Checklist

1. **Environment Audit**: Ensure all production secrets (`JWT_SECRET`, DB passwords) are loaded via environment manager / secret vault.
2. **License Register Verification**: Confirm no prohibited dependencies exist in `docs/dependency-license-register.md`.
3. **Database Migrations**: Execute relational schema migration scripts.
4. **SSL/TLS & HTTP Headers**: Verify HTTPS termination and CSP / HSTS header configuration.
