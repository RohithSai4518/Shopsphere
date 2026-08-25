# ShopSphere — Enterprise Python Full-Stack Marketplace Platform

[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-5.1-success.svg)](https://www.djangoproject.com/)
[![License Audit](https://img.shields.io/badge/License-100%25%20BSD%2FMIT-green.svg)](file:///DEPENDENCY_REGISTER.md)

ShopSphere is an independent, Amazon-inspired e-commerce marketplace platform built entirely with a **Python-First Full-Stack Architecture**. It features server-rendered Django Templates, Django ORM database layer, custom domain business services, multi-merchant seller management, double-entry inventory ledgering, atomic checkout state machines, and complete security controls.

---

## 🌟 Key Architecture & Highlights

- **Python-First Engine**: Django 5.1, Python 3.12, SQLite / PostgreSQL. Zero Node.js, Express, or React frontend code.
- **36 Relational Models**: Normalized database schema spanning 16 domain applications.
- **Multi-Merchant Marketplace**: Seller profiles, commission rate tracking, ratings, and order item fulfillment queue.
- **Inventory Ledger**: Real-time stock reservation, restock transaction logs, warehouse location tracking.
- **Promotions & Coupons**: Percentage and fixed discount codes with minimum order subtotal validation.
- **Strict License Policy**: 100% zero copyleft compliance (BSD-3-Clause, MIT, ISC, PSF).

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ installed
- Virtual environment (optional)

### 2. Environment Setup
```bash
# Clone or enter repository
cd Amazon_Clone

# Install dependencies (Strictly pinned MIT/BSD licenses)
pip install -r requirements.txt

# Create local environment configuration
copy .env.example .env
```

### 3. Database Initialization & Seeding
```bash
# Run Django database migrations
python manage.py migrate

# Seed synthetic marketplace database across 36 entities
python manage.py seed_shopsphere
```

### 4. Running Local Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

---

## 🧪 Automated Testing & Audit Verification

### Run Complete Test Suite
```bash
python manage.py test tests
```

### Run License Compliance Audit
```bash
python scripts/license_audit.py
```

### Measure Meaningful Source LOC
```bash
python scripts/count_loc.py
```

---

## 🔐 Credentials & Synthetic Accounts

- **Platform Admin**: `admin@shopsphere.local` / `AdminPass123!`
- **Merchant Seller**: `merchant@apextech.com` / `SellerPass123!`
- **Customer User**: `jane.customer@example.com` / `CustomerPass123!`
