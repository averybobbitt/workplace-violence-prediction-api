"""
Django settings for WorkplaceViolencePredictionAPI project.

This module contains settings and configurations for the Django project.

For more information on Django settings, see:
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see:
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

import toml

# Load configuration from config.toml
with open("config.toml", "r") as f:
    config = toml.load(f)

# Define global variables
DATA_SOURCES = config.get("data_sources")

if DATA_SOURCES is None:
    raise Exception("No data source configuration defined in config.toml")

DATA_SOURCES_BULK = DATA_SOURCES.get("bulk_samples")
DATA_SOURCES_NEW = DATA_SOURCES.get("new_sample")

LOCAL_API_KEY = config.get("auth").get("bearer")

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# Generate a random secret key
SECRET_KEY = os.urandom(24).hex()

# Debugging settings
DEBUG = os.environ.get("DJANGO_DEBUG", False)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "smtp.gmail.com"]

# Application definition
INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    "rest_framework.authtoken",
    "drf_spectacular",
    "corsheaders",
    # Local apps
    "WorkplaceViolencePredictionAPI.API",
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

ROOT_URLCONF = "WorkplaceViolencePredictionAPI.urls"

# Template settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Logging settings
LOGS_PATH = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGS_PATH):
    os.mkdir(LOGS_PATH)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOGS_PATH, "log.log"),
        },
        "console": {
            "class": "logging.StreamHandler",
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        }
    },
}

# Documentation settings
DOCUMENTATION_PATH = os.path.join(BASE_DIR, "WorkplaceViolencePredictionAPI", "docs")

# Application settings
WSGI_APPLICATION = "WorkplaceViolencePredictionAPI.wsgi.application"
ASGI_APPLICATION = "WorkplaceViolencePredictionAPI.asgi.application"

# Database settings
db_config = config.get("database")
if db_config is None:
    raise Exception("No database configuration defined in config.toml")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": db_config.get("database"),
        "USER": db_config.get("user"),
        "PASSWORD": db_config.get("password"),
        "HOST": db_config.get("host"),
        "PORT": "3306",
    }
}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# REST Framework settings
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Internationalization settings
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files settings
STATIC_ROOT = BASE_DIR / "static/"
STATIC_URL = "static/"

# Default primary key field type setting
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Redirect settings after login and logout
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# Session settings
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"

# drf_spectacular settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Workplace Violence Prediction API",
    "DESCRIPTION": "An automated system to predict potential incidents of workplace violence in a hospital",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# Email notification settings
EMAIL_CONFIG = config.get("email")

if EMAIL_CONFIG is None:
    raise Exception("No email configuration defined in config.toml")

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = EMAIL_CONFIG.get("sender")
EMAIL_HOST_PASSWORD = EMAIL_CONFIG.get("password")
