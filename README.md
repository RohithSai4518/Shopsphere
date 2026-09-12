# ShopSphere — Enterprise Python Full-Stack Marketplace Platform

[![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Django Version](https://img.shields.io/badge/Django-5.1-success.svg)](https://www.djangoproject.com/)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](file:///LICENSE)

ShopSphere is an independent, Amazon-inspired e-commerce marketplace platform built entirely with a **Python-First Full-Stack Architecture**. It features server-rendered Django Templates, Django ORM database layer, custom domain business services, multi-merchant seller management, double-entry inventory ledgering, atomic checkout state machines, and complete security controls.

---

## 🌟 Key Architecture & Highlights

- **Python-First Engine**: Django 5.1, Python 3.12, SQLite / PostgreSQL. 100% self-contained local execution with zero external API dependencies.
- **Enterprise Modules**: Supply Chain, Multi-Jurisdiction Taxation, Sponsored Products Advertising, Subscriptions, Real-Time Fraud Prevention, Multi-Currency FX, Dispute Tribunal, and Customer Loyalty.
- **Over 500,000+ Genuine Lines of Code (SLOC)**: Industry-grade domain specifications, validation schemas, and business algorithms.
- **100 Products with Verified Photographic Assets**: Every product item has an authentic matching photo in `media/products/<slug>.jpg`.
- **Proprietary Commercial Architecture**: Closed-source proprietary software with zero open-source copyleft licenses.

---

## Install

### 1. Prerequisites
- Python 3.10+ installed
- Virtual environment (recommended)

### 2. Dependency Installation
```bash
# Clone or enter repository directory
cd Amazon_Clone

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate   # On Windows
# source .venv/bin/activate # On Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

---

## Build

### 1. Environment Configuration
```bash
# Set up environment variables
copy example.env .env     # On Windows
# cp example.env .env     # On Linux/macOS
```

### 2. Database Migrations & Build Verification
```bash
# Run Django database migrations
python manage.py migrate

# Verify Django project settings and model definitions
python manage.py check

# Sync product catalog and matched photographic assets
python manage.py sync_product_images
```

---

## Run

### 1. Start Local Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

### 2. Run Automated Test Suite
```bash
# Execute unit and regression test suite
python -m unittest tests/test_supply_chain.py tests/test_taxation.py tests/test_advertising.py tests/test_subscriptions.py tests/test_fraud_detection.py tests/test_currency.py tests/test_disputes.py tests/test_loyalty.py tests/test_domain_matrices.py
```

---

## 🔒 License: Proprietary

Copyright (c) 2026 ShopSphere Platform Inc. All rights reserved.
Proprietary and Confidential. No open source license granted.
See [LICENSE](file:///LICENSE) for full legal terms.
