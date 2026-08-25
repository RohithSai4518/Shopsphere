# ShopSphere Deployment Guide

## Production Architecture
ShopSphere is configured for production deployment using **Python 3.12**, **Django 5.1**, Gunicorn/WSGI, and Docker containers.

---

## Container Deployment (Docker & Docker Compose)

### 1. Build and Launch Container
```bash
docker-compose up -d --build
```

### 2. Run Database Migrations in Container
```bash
docker-compose exec shopsphere python manage.py migrate
```

### 3. Seed Database Data in Container
```bash
docker-compose exec shopsphere python manage.py seed_shopsphere
```

---

## Environment Variable Production Configuration

Configure the following variables in `.env`:
```ini
DJANGO_SECRET_KEY=generate_a_random_64_character_secret_key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=shopsphere_prod
DATABASE_USER=shopsphere_pguser
DATABASE_PASSWORD=secure_postgres_password
DATABASE_HOST=postgres_host
DATABASE_PORT=5432
```
