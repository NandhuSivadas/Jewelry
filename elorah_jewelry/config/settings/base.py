import os
from pathlib import Path
from datetime import timedelta
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialize environ
env = environ.Env(
    DEBUG=(bool, False)
)

# Reading .env file if it exists
env_file = BASE_DIR / '.env'
if env_file.exists():
    environ.Env.read_env(env_file)

SECRET_KEY = env('SECRET_KEY', default='unsafe-secret-key-for-dev')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[])

INSTALLED_APPS = [
    "unfold",
    # Django built-in
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
    # Third-party
    "django_extensions",
    "django_filters",
    "django_htmx",
    "django_celery_beat",
    "axes",
    "csp",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "mptt",
    # Project apps (order matters for dependencies)
    "apps.core",
    "apps.audit",
    "apps.accounts",
    "apps.catalog",
    "apps.pricing",
    "apps.cart",
    "apps.orders",
    "apps.payments",
    "apps.promotions",
    "apps.wishlist",
    "apps.reviews",
    # "apps.notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",       # Static files
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_otp.middleware.OTPMiddleware",              # 2FA
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
    "axes.middleware.AxesMiddleware",                   # Brute-force
    "apps.core.middleware.RequestIDMiddleware",         # Request tracking
    "apps.core.middleware.MaintenanceMiddleware",       # Maintenance mode
    "apps.audit.middleware.AuditMiddleware",            # Capture request meta
    "csp.middleware.CSPMiddleware",                     # Content-Security-Policy
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {
        "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
            "apps.core.context_processors.site_config",
            "apps.cart.context_processors.cart_count",
        ],
    },
}]

WSGI_APPLICATION = "config.wsgi.application"

# Database
DATABASES = {
    "default": {
        **env.db("DATABASE_URL", default="postgres://elorah_user:pass@localhost:5432/elorah_jewelry"),
        "CONN_MAX_AGE": 600,
        "CONN_HEALTH_CHECKS": True,
    }
}

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env("REDIS_URL", default="redis://localhost:6379/0"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "elorah",
        "TIMEOUT": 300,  # 5 min default
    }
}

# Session (DB-backed for security, cache for performance)
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 86400          # 24 hours
SESSION_SAVE_EVERY_REQUEST = True   # Extend on activity
SESSION_COOKIE_NAME = "elorah_sid"

# Celery
CELERY_BROKER_URL = env("REDIS_URL", default="redis://localhost:6379/1")
CELERY_RESULT_BACKEND = env("REDIS_URL", default="redis://localhost:6379/2")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Asia/Kolkata"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300        # 5 min hard limit
CELERY_TASK_SOFT_TIME_LIMIT = 240   # 4 min soft limit
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Custom User Model
AUTH_USER_MODEL = "accounts.CustomUser"

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",  # Must be first for axes
    "django.contrib.auth.backends.ModelBackend",
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",  # Primary
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",  # Fallback for migration
]

# Static & Media
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# django-axes
AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = timedelta(minutes=30)
AXES_LOCKOUT_PARAMETERS = ["ip_address", "username"]
AXES_RESET_ON_SUCCESS = True
AXES_ENABLE_ACCESS_FAILURE_LOG = True

# Admin
ADMIN_URL_PREFIX = env("ADMIN_URL_PREFIX", default="management")
WEBHOOK_URL_PREFIX = env("WEBHOOK_URL_PREFIX", default="wh-callbacks")

# Store defaults
STORE_NAME = env("STORE_NAME", default="Elorah Jewelry")
STORE_STATE = env("STORE_STATE", default="Kerala")

# Sites Framework
SITE_ID = 1

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "sensitive_data": {
            "()": "apps.core.logging_filters.SensitiveDataFilter",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[{asctime}] [{levelname}] [{name}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["sensitive_data"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

UNFOLD = {
    "SITE_TITLE": "Elorah Jewelry Admin",
    "SITE_HEADER": "Elorah Admin",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: "/static/favicon.ico",
        "dark": lambda request: "/static/favicon.ico",
    },
    "COLORS": {
        "primary": {
            "50": "#FFF9E6",
            "100": "#FFF0B3",
            "200": "#FFE066",
            "300": "#FFD700",
            "400": "#DAA520",
            "500": "#B8860B",
            "600": "#996515",
            "700": "#7A4F0E",
            "800": "#5C3A08",
            "900": "#3D2605",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
    },
    "STYLES": [
        lambda request: "/static/css/admin_custom.css",
    ],
}
