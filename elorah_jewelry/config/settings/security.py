# All security settings in one auditable file

# Password Validators
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 10}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Security Headers
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# CSP (django-csp)
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'",)  # No 'unsafe-inline' — use nonce
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # Tailwind needs inline
CSP_IMG_SRC = ("'self'", "data:", "https://razorpay.com")
CSP_FONT_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'", "https://api.razorpay.com")
CSP_FRAME_SRC = ("'self'", "https://api.razorpay.com")  # Razorpay checkout modal
CSP_BASE_URI = ("'self'",)
CSP_FORM_ACTION = ("'self'",)

# Cookie Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"

# Login settings
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Rate limiting defaults
RATELIMIT_ENABLE = True
RATELIMIT_USE_CACHE = "default"
