"""
Django settings for restaurant_system project.

This file contains all the configuration for our Restaurant Ordering System.
It's beginner-friendly with comments explaining each section.
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================
# SECURITY SETTINGS
# ==============================================================

# SECURITY WARNING: keep the secret key used in production secret!
# In production (Render), we will set this using an environment variable.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-change-this-key-in-production-1234567890'
)

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG is True locally, but False on Render (set via environment variable).
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['54.211.188.243']

# Allow all hosts if DEBUG is False and RENDER_EXTERNAL_HOSTNAME is set
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

if DEBUG:
    ALLOWED_HOSTS += ['localhost', '127.0.0.1']


# ==============================================================
# APPLICATION DEFINITION
# ==============================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our custom apps
    'accounts',
    'menu',
    'cart',
    'orders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise serves static files in production (right after SecurityMiddleware)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'restaurant_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # We use a project-level templates folder (not just app-level)
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processor to make cart count available on every page
                'cart.context_processors.cart_item_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'restaurant_system.wsgi.application'


# ==============================================================
# DATABASE
# ==============================================================

# Default: SQLite (used for local development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# On Render, DATABASE_URL environment variable will override this
# (Render can provide a PostgreSQL database, but SQLite also works for small apps)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    DATABASES['default'] = dj_database_url.parse(DATABASE_URL)


# ==============================================================
# PASSWORD VALIDATION
# ==============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================
# INTERNATIONALIZATION
# ==============================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================
# STATIC FILES (CSS, JavaScript, Images)
# ==============================================================

STATIC_URL = '/static/'
# Where Django looks for static files during development
STATICFILES_DIRS = [BASE_DIR / 'static']
# Where 'collectstatic' will gather files for production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise compressed storage for production performance
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ==============================================================
# MEDIA FILES (User-uploaded images like food photos)
# ==============================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==============================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================
# LOGIN / LOGOUT REDIRECTS
# ==============================================================

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


# ==============================================================
# MESSAGE TAGS (so Bootstrap alert classes match Django messages)
# ==============================================================

from django.contrib.messages import constants as messages_constants

MESSAGE_TAGS = {
    messages_constants.DEBUG: 'secondary',
    messages_constants.INFO: 'info',
    messages_constants.SUCCESS: 'success',
    messages_constants.WARNING: 'warning',
    messages_constants.ERROR: 'danger',
}