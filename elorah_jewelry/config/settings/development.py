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
