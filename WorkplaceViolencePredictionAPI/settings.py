"""
Django settings for WorkplaceViolencePredictionAPI project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path

import toml

# Define global variables
with open("config.toml", "r") as f:
    config = toml.load(f)

DATA_SOURCES = config.get("data_sources")

if DATA_SOURCES is None:
    raise Exception("No data source configuration defined in config.toml")

DATA_SOURCES_BULK = DATA_SOURCES.get("bulk_samples")
DATA_SOURCES_NEW = DATA_SOURCES.get("new_sample")

LOCAL_API_KEY = config.get("auth").get("bearer")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-2zok5=*3&%3w50fcwpxeug49)tmz-(@9g=n%3q*%x_p==9)^rp'
SECRET_KEY = os.urandom(24).hex()

# Check if application is running in a development environment
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", False)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "smtp.gmail.com"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "WorkplaceViolencePredictionAPI.API",
    "drf_spectacular"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "WorkplaceViolencePredictionAPI.urls"

# It is important to note APP_DIRS is set to true here, this makes the template loader
# search for a "templates" subdir in all app directories for apps defined in INSTALLED_APPS
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

DOCUMENTATION_PATH = os.path.join(BASE_DIR, "WorkplaceViolencePredictionAPI", "openapi.json")

WSGI_APPLICATION = "WorkplaceViolencePredictionAPI.wsgi.application"
ASGI_APPLICATION = "WorkplaceViolencePredictionAPI.asgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

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

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# REST Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
# Similarly to TEMPLATES above, Django will search for a "static" subdir in all app directories
STATIC_ROOT = BASE_DIR / "static/"
STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Settings for drf_spectacular (an OpenAPI doc generator)
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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_SENDER = EMAIL_CONFIG.get("sender")
EMAIL_HOST_PASSWORD = EMAIL_CONFIG.get("password")
EMAIL_RECIPIENTS = EMAIL_CONFIG.get("recipients")
