from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Email - print to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# We don't want to enforce secure cookies in dev
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Import security settings but we can relax some for dev if needed
from .security import *

# Override CACHES for local development to not require Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "elorah-local-cache",
    }
}

# Relax CSP for local development to allow CDNs (Tailwind, HTMX, Alpine) and inline scripts
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "'unsafe-eval'", "https://cdn.tailwindcss.com", "https://unpkg.com", "https://cdn.jsdelivr.net")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_IMG_SRC = ("'self'", "data:", "https://via.placeholder.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
