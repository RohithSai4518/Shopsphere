import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'synthetic_shopsphere_django_secret_key_2026_prod_secure_998877')

DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,0.0.0.0').split(',')]

# Installed Applications Architecture
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # ShopSphere Domain Apps
    'apps.accounts',
    'apps.rbac',
    'apps.catalog',
    'apps.cart',
    'apps.wishlist',
    'apps.orders',
    'apps.payments',
    'apps.inventory',
    'apps.sellers',
    'apps.reviews',
    'apps.promotions',
    'apps.returns',
    'apps.support',
    'apps.notifications',
    'apps.analytics',
    'apps.audit',
    'apps.administration',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.cart.context_processors.cart_summary',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Database Configuration (Supports DATABASE_URL for PostgreSQL / Neon, falls back to SQLite)
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and (DATABASE_URL.startswith('postgres://') or DATABASE_URL.startswith('postgresql://')):
    import urllib.parse
    parsed_db = urllib.parse.urlparse(DATABASE_URL)
    query_params = urllib.parse.parse_qs(parsed_db.query)
    
    db_options = {}
    if 'sslmode' in query_params:
        db_options['sslmode'] = query_params['sslmode'][0]
    if 'channel_binding' in query_params:
        db_options['channel_binding'] = query_params['channel_binding'][0]

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parsed_db.path.lstrip('/'),
            'USER': parsed_db.username,
            'PASSWORD': parsed_db.password,
            'HOST': parsed_db.hostname,
            'PORT': parsed_db.port or 5432,
            'OPTIONS': db_options,
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
            'NAME': os.path.join(BASE_DIR, os.getenv('DATABASE_NAME', 'data/shopsphere_django.sqlite3')),
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media Files Architecture
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Session & Security Settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 86400 * 7
CSRF_COOKIE_HTTPONLY = True

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
