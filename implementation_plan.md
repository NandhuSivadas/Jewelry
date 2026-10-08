# Elorah Jewelry — Implementation Plan (Resumable)

> **PURPOSE**: This is the master implementation tracker. If you (the agent) run
> out of quota and resume later, **read this file first**. Find the
> `CURRENT STATUS` section, then continue from the next unchecked item.

---

## 🔴 CURRENT STATUS

```
PHASE:     Phase 2 — BUILD
STEP:      Not started
SUB-TASK:  Not started
LAST FILE: N/A
BLOCKER:   Awaiting user approval to begin
```

**Update this section every time a sub-task is completed.**

---

## Quick Reference (Confirmed Decisions)

| Key | Value |
|---|---|
| Project name | `elorah_jewelry` |
| Brand | Elorah Jewelry |
| Python | 3.12 |
| Django | 5.1.x |
| Database | PostgreSQL 16 |
| Cache/Broker | Redis 7 |
| Task queue | Celery |
| Password hasher | Argon2 |
| Payments | Razorpay (behind abstraction layer) |
| Image storage | Local filesystem (Nginx-served in prod; cloud-ready for future) |
| Email | Gmail SMTP (initially) |
| Frontend | Django templates + Tailwind CSS + HTMX |
| Seller state | Kerala |
| Currency | INR |
| Default GST | 3% gold/silver (HSN 7113), 5% imitation (HSN 7117) |
| GST management | Fully admin-configurable (GSTConfig model) |
| Pricing modes | DYNAMIC (precious metals), FIXED (imitation) |
| Guest checkout | Yes |
| COD max | ₹50,000 (admin-configurable) |
| Free shipping | Above ₹2,000 (admin-configurable) |
| Shipping | Zone-based flat rate |
| Max qty/product | 5 per order |
| Coupon stacking | One per order |
| Cancellation | Before PROCESSING only (customer); admin anytime |
| Returns | 7 days, admin approval |
| Refunds | To original payment method |
| Admin URL | From env var (NOT /admin/) |
| Webhook URL | From env var (secret prefix) |
| Docker | Yes (dev + prod compose files) |
| CI | GitHub Actions |
| Workspace | `d:\Jewellary` |

---

## STEP 1: Config + Core Foundation

**Goal**: Working Django project with settings split, Celery, Redis, PostgreSQL,
health check, base templates, error pages, and core utilities.

### 1.1 — Project Initialization
- [ ] Create `elorah_jewelry/manage.py`
- [ ] Create `elorah_jewelry/config/__init__.py`
- [ ] Create `elorah_jewelry/config/wsgi.py`
- [ ] Create `elorah_jewelry/config/asgi.py`
- [ ] Create `elorah_jewelry/apps/__init__.py`

**Files**: `manage.py`, `config/__init__.py`, `config/wsgi.py`, `config/asgi.py`, `apps/__init__.py`

### 1.2 — Requirements Files
- [ ] Create `requirements/base.txt` (all shared deps, pinned)
- [ ] Create `requirements/development.txt` (inherits base + dev tools)
- [ ] Create `requirements/production.txt` (inherits base + gunicorn)

**Files**: `requirements/base.txt`, `requirements/development.txt`, `requirements/production.txt`

### 1.3 — Environment Configuration
- [ ] Create `.env.example` with ALL variables documented
- [ ] Create `.gitignore` (comprehensive: .env, media, __pycache__, etc.)
- [ ] Create `.dockerignore`
- [ ] Create `pyproject.toml` (black, isort, ruff config)
- [ ] Create `pytest.ini`
- [ ] Create `Makefile` (common commands)

**Files**: `.env.example`, `.gitignore`, `.dockerignore`, `pyproject.toml`, `pytest.ini`, `Makefile`

**`.env.example` must include**:
```
DJANGO_SETTINGS_MODULE, SECRET_KEY, DEBUG,
ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS,
DATABASE_URL (postgres://),
REDIS_URL,
RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET, RAZORPAY_WEBHOOK_SECRET,

EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
SENTRY_DSN,
ADMIN_URL_PREFIX, WEBHOOK_URL_PREFIX,
STORE_NAME, STORE_GSTIN, STORE_STATE, STORE_EMAIL, STORE_PHONE,
SITE_DOMAIN
```

### 1.4 — Settings Split
- [ ] Create `config/settings/__init__.py`
- [ ] Create `config/settings/base.py`
  - INSTALLED_APPS (all apps registered as `apps.<name>`)
  - MIDDLEWARE stack (ordered correctly)
  - AUTH_USER_MODEL = `accounts.CustomUser`
  - PASSWORD_HASHERS (Argon2 first)
  - Database: PostgreSQL via `DATABASE_URL`
  - Cache: Redis via `REDIS_URL`
  - Celery config (broker, result backend, timezone)
  - Templates config (dirs, context_processors)
  - Static/media config
  - Logging config (structured, rotating)
  - django-axes config
  - Session: database-backed or cache-backed
  - All settings read from env via django-environ
- [ ] Create `config/settings/development.py`
  - DEBUG=True
  - django-debug-toolbar
  - Console email backend
  - Relaxed but still-present security settings
- [ ] Create `config/settings/production.py`
  - DEBUG=False enforced
  - Imports security.py
  - Strict ALLOWED_HOSTS
  - Local file system storage via Nginx for media files
  - Sentry init
  - WhiteNoise
  - Secure cookies, HSTS, etc.
- [ ] Create `config/settings/security.py`
  - CSP directives (django-csp)
  - Session cookie config
  - CSRF config
  - Security headers
  - Password validators
  - Rate limit defaults

**Files**: `config/settings/__init__.py`, `base.py`, `development.py`, `production.py`, `security.py`

### 1.5 — Celery Configuration
- [ ] Create `config/celery.py` (app init, autodiscover_tasks)
- [ ] Update `config/__init__.py` (import celery app)

**Files**: `config/celery.py`, update `config/__init__.py`

### 1.6 — URL Routing (Split)
- [ ] Create `config/urls/__init__.py` (root urlconf, includes public + internal + webhooks)
- [ ] Create `config/urls/public.py` (customer-facing routes)
- [ ] Create `config/urls/internal.py` (admin panel, env-prefix)
- [ ] Create `config/urls/webhooks.py` (payment webhooks, env-prefix)

**Files**: `config/urls/__init__.py`, `public.py`, `internal.py`, `webhooks.py`

### 1.7 — Core App
- [ ] Create `apps/core/__init__.py`
- [ ] Create `apps/core/apps.py` (label = `core`)
- [ ] Create `apps/core/models.py` (SiteConfig singleton model)
- [ ] Create `apps/core/mixins.py` (TimestampMixin, SlugMixin)
- [ ] Create `apps/core/utils.py` (INR formatting, random filename, etc.)
- [ ] Create `apps/core/validators.py` (shared validators)
- [ ] Create `apps/core/exceptions.py` (custom exception hierarchy)
- [ ] Create `apps/core/context_processors.py` (site config, cart count placeholder, year)
- [ ] Create `apps/core/middleware.py` (RequestID middleware)
- [ ] Create `apps/core/views.py` (home placeholder, health check, legal pages)
- [ ] Create `apps/core/urls.py`
- [ ] Create `apps/core/templatetags/__init__.py`
- [ ] Create `apps/core/templatetags/core_tags.py` (INR filter, etc.)
- [ ] Create `apps/core/admin.py` (SiteConfig admin)
- [ ] Create `apps/core/management/__init__.py`
- [ ] Create `apps/core/management/commands/__init__.py`
- [ ] Create `apps/core/migrations/` (empty __init__.py)

**Files**: 17 files under `apps/core/`

### 1.8 — Base Templates & Error Pages
- [ ] Create `templates/base.html` (master layout: Tailwind, HTMX, Elorah branding)
- [ ] Create `templates/partials/_navbar.html`
- [ ] Create `templates/partials/_footer.html`
- [ ] Create `templates/partials/_messages.html`
- [ ] Create `templates/partials/_breadcrumbs.html`
- [ ] Create `templates/partials/_pagination.html`
- [ ] Create `templates/partials/_seo_meta.html`
- [ ] Create `templates/partials/_trust_badges.html`
- [ ] Create `templates/errors/400.html`
- [ ] Create `templates/errors/403.html`
- [ ] Create `templates/errors/404.html`
- [ ] Create `templates/errors/500.html`
- [ ] Create `templates/core/home.html` (placeholder homepage)
- [ ] Create `templates/core/health.html` (optional, health can be JSON)
- [ ] Create `templates/legal/privacy_policy.html`
- [ ] Create `templates/legal/terms_conditions.html`
- [ ] Create `templates/legal/shipping_policy.html`
- [ ] Create `templates/legal/return_policy.html`
- [ ] Create `templates/legal/refund_policy.html`

**Files**: 19 template files

### 1.9 — Static Files (Initial)
- [ ] Create `static/css/input.css` (Tailwind source with Elorah theme)
- [ ] Create `static/js/main.js` (minimal: mobile menu toggle, message dismiss)
- [ ] Create `tailwind.config.js` (Elorah palette: gold, black, cream/ivory)

**Files**: `static/css/input.css`, `static/js/main.js`, `tailwind.config.js`

### 1.10 — Docker (Dev)
- [ ] Create `docker/Dockerfile` (multi-stage, non-root)
- [ ] Create `docker/docker-entrypoint.sh`
- [ ] Create `docker-compose.yml` (web, postgres, redis)

**Files**: `docker/Dockerfile`, `docker/docker-entrypoint.sh`, `docker-compose.yml`

### 1.11 — Verification
- [ ] Run `pip install -r requirements/development.txt`
- [ ] Run `python manage.py check`
- [ ] Run `python manage.py makemigrations core`
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py runserver` — verify health endpoint responds
- [ ] Verify base template renders (home page loads)
- [ ] Verify error pages (404, 500)
- [ ] Write and run basic tests for health check + SiteConfig

**Commands**:
```bash
python manage.py check
python manage.py makemigrations core
python manage.py migrate
python manage.py test apps.core
# or: pytest apps/core/tests/
```

### 1.12 — Summary & Handoff
- [ ] Update CURRENT STATUS in this file
- [ ] Summarize what was built
- [ ] List any risks found
- [ ] WAIT for user go-ahead

---

## STEP 2: Accounts App

**Goal**: Custom user model (email as username), registration, login, logout,
email verification, password reset, profile, multiple addresses, 2FA for staff.

### 2.1 — Models
- [ ] Create `apps/accounts/__init__.py`
- [ ] Create `apps/accounts/apps.py`
- [ ] Create `apps/accounts/managers.py` (CustomUserManager)
- [ ] Create `apps/accounts/models.py` (CustomUser, UserProfile, Address)
  - CustomUser: email (USERNAME_FIELD), phone, is_email_verified, Argon2
  - UserProfile: OneToOne, dob, gender, avatar, newsletter
  - Address: user FK, label, full_name, phone, lines, city, state, pincode, defaults
- [ ] Create migrations and migrate

### 2.2 — Forms
- [ ] Create `apps/accounts/forms.py`
  - RegistrationForm (email, name, phone, password, confirm password)
  - LoginForm (email, password)
  - ProfileForm, AddressForm
  - PasswordResetForm, PasswordChangeForm

### 2.3 — Services & Validators
- [ ] Create `apps/accounts/services.py`
  - register_user() — create user + profile, send verification email
  - verify_email() — token validation
  - merge_cart_on_login() — placeholder (implemented in cart step)
- [ ] Create `apps/accounts/validators.py`
  - Phone number validator (Indian format)
  - Custom password validators (if extending Django defaults)
- [ ] Create `apps/accounts/selectors.py`

### 2.4 — Views & URLs
- [ ] Create `apps/accounts/views.py`
  - RegisterView, LoginView, LogoutView
  - EmailVerificationView, ResendVerificationView
  - PasswordResetView, PasswordResetConfirmView
  - ProfileView, ProfileUpdateView
  - AddressListView, AddressCreateView, AddressUpdateView, AddressDeleteView
  - OrderHistoryView (placeholder — wired in orders step)
- [ ] Create `apps/accounts/urls.py`
- [ ] Wire into `config/urls/public.py`

### 2.5 — Templates
- [ ] Create `templates/accounts/register.html`
- [ ] Create `templates/accounts/login.html`
- [ ] Create `templates/accounts/logout.html`
- [ ] Create `templates/accounts/verify_email.html`
- [ ] Create `templates/accounts/password_reset.html`
- [ ] Create `templates/accounts/password_reset_confirm.html`
- [ ] Create `templates/accounts/password_reset_done.html`
- [ ] Create `templates/accounts/profile.html`
- [ ] Create `templates/accounts/address_list.html`
- [ ] Create `templates/accounts/address_form.html`
- [ ] Create `templates/accounts/dashboard.html`

### 2.6 — Admin
- [ ] Create `apps/accounts/admin.py` (CustomUser admin, Address inline)

### 2.7 — Signals & Middleware
- [ ] Create `apps/accounts/signals.py` (create profile on user creation)
- [ ] Create `apps/accounts/middleware.py` (last activity tracking)

### 2.8 — Security
- [ ] Generic error messages on login/reset (no account enumeration)
- [ ] django-axes integration (brute-force protection on login)
- [ ] Rate limiting on register, password reset
- [ ] IDOR protection: all address/profile views filter by request.user
- [ ] Safe `next` parameter handling (same-origin only)

### 2.9 — Tests
- [ ] Create `apps/accounts/tests/__init__.py`
- [ ] Create `apps/accounts/tests/factories.py` (UserFactory, AddressFactory)
- [ ] Create `apps/accounts/tests/test_models.py`
- [ ] Create `apps/accounts/tests/test_views.py`
  - Registration (valid, duplicate email, weak password)
  - Login (valid, wrong password, locked out after N attempts)
  - Email verification
  - Password reset
  - Profile update
  - Address CRUD
- [ ] Create `apps/accounts/tests/test_services.py`
- [ ] Create `apps/accounts/tests/test_idor.py`
  - User A cannot view/edit/delete User B's addresses
  - User A cannot view User B's profile
- [ ] Create `apps/accounts/tests/test_permissions.py`

### 2.10 — Verification
- [ ] `python manage.py check`
- [ ] `python manage.py makemigrations accounts`
- [ ] `python manage.py migrate`
- [ ] `pytest apps/accounts/tests/ -v`
- [ ] Manual smoke test: register, login, add address, logout
- [ ] Update CURRENT STATUS
- [ ] WAIT for user go-ahead

---

## STEP 3: Catalog App

**Goal**: Categories (nested), products, variants, images (secure upload),
flexible attributes (EAV), stock records, search, filters, pagination.

### 3.1 — Models
- [ ] Create `apps/catalog/` boilerplate (`__init__`, `apps.py`)
- [ ] Create `apps/catalog/models.py`
  - Category (MPTT: name, slug, parent, image, meta, is_active, sort_order)
  - Material (name, slug, is_precious, is_active)
  - Purity (material FK, name, code, purity_percentage)
  - Product (all fields from plan — name, slug, sku, category, material,
    purity, pricing_mode, base_price, weights, making charge, stone charge,
    hallmark, hsn_code, flags, meta, views_count, timestamps)
  - ProductImage (product FK, image, webp, thumbnail, alt, is_primary, order)
  - ProductVariant (product FK, sku, name, size, color, purity override,
    weight override, price adjustment, is_active)
  - StockRecord (product FK, variant FK, quantity, reserved, threshold)
  - AttributeDefinition (category FK, name, slug, type, choices, required, filterable)
  - AttributeValue (product FK, attribute FK, value_text/number/boolean)
- [ ] Create `apps/catalog/managers.py` (ActiveProductManager, FeaturedManager)
- [ ] Run migrations

### 3.2 — Image Security
- [ ] Create `apps/catalog/image_utils.py`
  - validate_image_extension()
  - validate_image_mime() — python-magic
  - validate_image_size() — max 5MB
  - validate_image_dimensions() — max 4096×4096
  - process_image() — Pillow re-encode, strip metadata
  - generate_thumbnail() — 300×300
  - generate_webp()
  - generate_safe_filename() — uuid4 + extension

### 3.3 — Services & Selectors
- [ ] Create `apps/catalog/services.py`
  - StockService: check_availability, reserve, release, deduct
  - ImageService: process_and_save (runs security pipeline)
- [ ] Create `apps/catalog/selectors.py`
  - get_product_list() — with select_related/prefetch_related
  - get_product_detail() — full join with images, variants, attributes
  - get_featured_products()
  - get_new_arrivals()
  - get_related_products()
  - search_products()

### 3.4 — Filters
- [ ] Create `apps/catalog/filters.py`
  - ProductFilter: category, price range, material, purity, size, in_stock

### 3.5 — Views & URLs
- [ ] Create `apps/catalog/views.py`
  - CategoryListView, CategoryDetailView (product listing by category)
  - ProductListView (search, filter, sort, paginate)
  - ProductDetailView (images, variants, attributes, related, reviews placeholder)
- [ ] Create `apps/catalog/urls.py`
- [ ] Wire into public URLs

### 3.6 — Templates
- [ ] Create `templates/catalog/category_list.html`
- [ ] Create `templates/catalog/product_list.html` (grid, filters sidebar)
- [ ] Create `templates/catalog/product_detail.html` (gallery, variants, add-to-cart)
- [ ] Create `templates/catalog/partials/_product_card.html`
- [ ] Create `templates/catalog/partials/_filters.html`
- [ ] Create `templates/catalog/partials/_sort_bar.html`

### 3.7 — Admin
- [ ] Create `apps/catalog/admin.py`
  - CategoryAdmin (MPTT drag-drop)
  - ProductAdmin (list filters, search, inline images + variants)
  - MaterialAdmin, PurityAdmin
  - StockRecordAdmin (low stock highlights)
  - Bulk actions: activate/deactivate

### 3.8 — Sitemaps & SEO
- [ ] Create `apps/catalog/sitemaps.py` (ProductSitemap, CategorySitemap)

### 3.9 — Tests
- [ ] Create `apps/catalog/tests/factories.py`
- [ ] Create `apps/catalog/tests/test_models.py`
  - Constraints: non-negative price, non-negative stock, unique SKU/slug
  - Category tree structure
- [ ] Create `apps/catalog/tests/test_views.py`
  - Product listing: pagination, filters, sorting
  - Product detail: all data loads
  - assertNumQueries on listing and detail pages
- [ ] Create `apps/catalog/tests/test_selectors.py`
- [ ] Create `apps/catalog/tests/test_image_utils.py`
  - Valid image accepted
  - Oversized image rejected
  - Non-image file rejected
  - Double extension rejected
  - SVG with script rejected
  - EXIF data stripped

### 3.10 — Verification
- [ ] `python manage.py check`
- [ ] `pytest apps/catalog/tests/ -v`
- [ ] Verify N+1 queries prevented (assertNumQueries)
- [ ] Update CURRENT STATUS
- [ ] WAIT for user go-ahead

---

## STEP 4: Pricing App

**Goal**: Metal rates (admin-managed, cached), GST config (fully admin-configurable),
PricingService (FIXED/DYNAMIC), TaxService, ShippingService, pincode check.

### 4.1 — Models
- [ ] Create `apps/pricing/` boilerplate
- [ ] Create `apps/pricing/models.py`
  - MetalRate (material, purity, rate_per_gram, effective_date, is_current, source, updated_by)
  - GSTConfig (name, hsn_code, description, tax_rate, applies_to, is_active,
    effective_from, effective_to, updated_by) — **fully admin-editable**
  - ShippingZone (name, is_active)
  - ShippingRate (zone, min/max order value, charge, free_shipping_threshold)
  - PincodeServiceability (pincode, zone, is_serviceable, cod_available, estimated_days)
- [ ] Run migrations

### 4.2 — Services
- [ ] Create `apps/pricing/services.py`
  - PricingService:
    - get_current_rate(material, purity) — Redis cached
    - compute_price(product, variant=None) → PriceBreakdown dataclass
    - snapshot_for_order(product, variant) → dict
  - TaxService:
    - get_active_gst_config(hsn_code) — from GSTConfig model
    - compute_tax(amount, hsn_code, seller_state, buyer_state) → TaxBreakdown
    - determine_cgst_sgst_igst(seller_state, buyer_state, rate) → dict
  - ShippingService:
    - check_pincode(pincode) → serviceability info
    - calculate_shipping(pincode, order_value) → Decimal
    - is_cod_available(pincode, order_value) → bool

### 4.3 — Selectors & Caching
- [ ] Create `apps/pricing/selectors.py`
  - get_current_metal_rates() — cached
  - invalidate_rate_cache() — called on MetalRate save

### 4.4 — Views & URLs
- [ ] Create `apps/pricing/views.py`
  - PincodeCheckView (HTMX — check serviceability, shipping cost, COD availability)
- [ ] Create `apps/pricing/urls.py`

### 4.5 — Admin
- [ ] Create `apps/pricing/admin.py`
  - MetalRateAdmin (list by material/purity, editable rate, history visible)
  - GSTConfigAdmin (full CRUD, change history, effective dates, descriptions)
  - ShippingZoneAdmin + ShippingRateAdmin (inline rates per zone)
  - PincodeServiceabilityAdmin (import-friendly, bulk edit)

### 4.6 — Template Tags
- [ ] Create `apps/pricing/templatetags/pricing_tags.py`
  - `{% product_price product %}` — renders formatted price
  - `{{ amount|inr }}` — INR formatting with Indian numbering
  - `{% tax_breakup order %}` — renders CGST/SGST/IGST breakup

### 4.7 — Tests
- [ ] Create `apps/pricing/tests/factories.py`
- [ ] Create `apps/pricing/tests/test_services.py`
  - FIXED pricing: base_price used directly
  - DYNAMIC pricing: rate × weight + making + stone
  - Making charge modes: FIXED, PER_GRAM, PERCENTAGE
  - Discount applied correctly
  - GST computed correctly (3%, 5%, custom)
  - CGST/SGST for intra-state (Kerala→Kerala)
  - IGST for inter-state (Kerala→Maharashtra)
  - Shipping calculation by zone
  - Free shipping threshold
  - COD availability check
  - Cache invalidation on rate update
- [ ] Create `apps/pricing/tests/test_models.py`

### 4.8 — Verification
- [ ] `python manage.py check`
- [ ] `pytest apps/pricing/tests/ -v`
- [ ] Update CURRENT STATUS
- [ ] WAIT for user go-ahead

---

## STEP 5: Cart App

**Goal**: Session cart (guests), DB cart (users), merge on login,
server-side totals, stock validation, tamper protection.

### 5.1 — Models
- [ ] Create `apps/cart/` boilerplate
- [ ] Create `apps/cart/models.py` (Cart, CartItem)
- [ ] Run migrations

### 5.2 — Services
- [ ] Create `apps/cart/services.py`
  - CartService:
    - get_or_create_cart(request) — session or DB
    - add_item(cart, product, variant, quantity) — validates stock
    - update_quantity(cart, item_id, quantity) — validates stock
    - remove_item(cart, item_id)
    - merge_carts(session_cart, user_cart) — on login
    - get_cart_totals(cart) — server-side recalculation using PricingService
    - validate_cart(cart) — check all items still available, prices correct
    - clear_cart(cart)

### 5.3 — Views, URLs, Context Processor
- [ ] Create `apps/cart/views.py`
  - CartDetailView (HTMX for quantity updates)
  - AddToCartView (POST only)
  - UpdateCartItemView (POST only)
  - RemoveCartItemView (POST only)
- [ ] Create `apps/cart/urls.py`
- [ ] Create `apps/cart/context_processors.py` (cart_count)
- [ ] Create `apps/cart/middleware.py` (ensure session key exists)

### 5.4 — Templates
- [ ] Create `templates/cart/cart_detail.html`
- [ ] Create `templates/cart/partials/_cart_item.html`
- [ ] Create `templates/cart/partials/_cart_summary.html`
- [ ] Create `templates/cart/partials/_empty_cart.html`

### 5.5 — Tests
- [ ] Create `apps/cart/tests/factories.py`
- [ ] Create `apps/cart/tests/test_services.py`
  - Add item, update qty, remove
  - Stock validation (cannot add more than available)
  - Merge guest cart into user cart on login
  - Totals calculated server-side (not from frontend)
- [ ] Create `apps/cart/tests/test_views.py`
- [ ] Create `apps/cart/tests/test_tamper.py`
  - Cannot send price from frontend
  - Cannot exceed stock via POST manipulation
  - Cannot add inactive/out-of-stock products

### 5.6 — Verification
- [ ] `python manage.py check`
- [ ] `pytest apps/cart/tests/ -v`
- [ ] Update CURRENT STATUS
- [ ] WAIT for user go-ahead

---

## STEP 6: Orders App

**Goal**: Order creation with full snapshots, state machine, status logs,
PDF invoices (GST-compliant), email notifications, cancellation flow.

### 6.1 — Models
- [ ] Create `apps/orders/` boilerplate
- [ ] Create `apps/orders/models.py`
  - OrderAddressSnapshot
  - Order (all fields from plan)
  - OrderItem (full product snapshot at purchase time)
  - OrderStatusLog
- [ ] Run migrations

### 6.2 — State Machine
- [ ] Create `apps/orders/state_machine.py`
  - VALID_TRANSITIONS dict
  - can_transition(from_status, to_status) → bool
  - transition_order(order, new_status, actor, note) — atomic, logs

  Valid transitions:
  ```
  PENDING     → CONFIRMED, CANCELLED
  CONFIRMED   → PROCESSING, CANCELLED
  PROCESSING  → SHIPPED, CANCELLED (admin only)
  SHIPPED     → DELIVERED
  DELIVERED   → RETURN_REQUESTED
  RETURN_REQUESTED → RETURNED, DELIVERED (rejected)
  ```

### 6.3 — Services
- [ ] Create `apps/orders/services.py`
  - OrderService:
    - create_order(user, cart, shipping_addr, billing_addr, payment_method, coupon) → Order
      - Validate cart (stock, prices)
      - Create address snapshots
      - Create order + order items with full product snapshots
      - Reserve stock (select_for_update)
      - Apply coupon
      - Calculate tax via TaxService
      - Calculate shipping via ShippingService
      - Generate order number (JW-YYYYMMDD-XXXX)
    - cancel_order(order, actor, reason)
    - request_return(order, actor, reason)
  - InvoiceService:
    - generate_invoice_pdf(order) — via WeasyPrint, GST-compliant

### 6.4 — Celery Tasks
- [ ] Create `apps/orders/tasks.py`
  - generate_invoice_task(order_id)
  - send_order_confirmation_email(order_id)
  - send_order_shipped_email(order_id)
  - send_order_delivered_email(order_id)

### 6.5 — Views & URLs
- [ ] Create `apps/orders/views.py`
  - CheckoutView (multi-step: address → review → payment)
  - OrderConfirmationView (success page)
  - OrderDetailView (tracking, status, items)
  - OrderListView (user's order history)
  - OrderCancelView
  - OrderInvoiceDownloadView
- [ ] Create `apps/orders/urls.py`

### 6.6 — Templates
- [ ] Create `templates/orders/checkout.html`
- [ ] Create `templates/orders/checkout_address.html`
- [ ] Create `templates/orders/checkout_review.html`
- [ ] Create `templates/orders/order_success.html`
- [ ] Create `templates/orders/order_detail.html`
- [ ] Create `templates/orders/order_list.html`
- [ ] Create `templates/orders/order_cancel.html`
- [ ] Create `templates/orders/invoice_template.html` (WeasyPrint, GST layout)

### 6.7 — Admin
- [ ] Create `apps/orders/admin.py`
  - OrderAdmin (list, filters, search, inline items, status update, CSV export)
  - Status change triggers state machine
  - Read-only audit fields

### 6.8 — Tests
- [ ] Create `apps/orders/tests/factories.py`
- [ ] Create `apps/orders/tests/test_services.py`
  - Order creation with correct snapshots
  - Snapshot integrity (change product after order → order unchanged)
  - Tax calculation in order
  - Shipping calculation in order
  - Order number generation (unique, human-readable)
- [ ] Create `apps/orders/tests/test_state_machine.py`
  - All valid transitions work
  - All invalid transitions raise error
  - Status log created on every transition
  - Actor recorded
- [ ] Create `apps/orders/tests/test_views.py`
  - Checkout flow end-to-end
  - IDOR: user A cannot view user B's order
  - Cannot checkout with empty cart
  - Cannot checkout with out-of-stock items
- [ ] Create `apps/orders/tests/test_snapshots.py`

### 6.9 — Verification
- [ ] `python manage.py check`
- [ ] `pytest apps/orders/tests/ -v`
- [ ] Update CURRENT STATUS
- [ ] WAIT for user go-ahead

---

## STEP 7: Payments App

**Goal**: Gateway abstraction, Razorpay integration, server-side verification,
webhooks with idempotency, COD support, stock management on payment events.

### 7.1 — Models
- [ ] Create `apps/payments/` boilerplate
- [ ] Create `apps/payments/models.py` (Payment with UUID PK, WebhookEvent)
- [ ] Run migrations

### 7.2 — Gateway Abstraction
- [ ] Create `apps/payments/gateway/__init__.py`
- [ ] Create `apps/payments/gateway/base.py` (PaymentGateway ABC)
- [ ] Create `apps/payments/gateway/razorpay.py` (RazorpayGateway)
  - create_order() — Razorpay API
  - verify_payment() — HMAC signature + amount verification
  - handle_webhook() — signature verification + event processing
  - initiate_refund() — Razorpay refund API
- [ ] Create `apps/payments/gateway/factory.py` (GatewayFactory)

### 7.3 — Services
- [ ] Create `apps/payments/services.py`
  - PaymentService:
    - initiate_payment(order) → {gateway_order_id, key, amount, ...}
    - verify_and_capture(order, payment_data) — atomic, stock, status
    - process_webhook(payload, signature) — idempotent
    - process_cod(order) — create COD payment record
    - initiate_refund(payment, amount) → refund result

### 7.4 — Webhook Handler
- [ ] Create `apps/payments/webhooks.py`
  - verify_webhook_signature()
  - check_idempotency(event_id) — dedup via WebhookEvent
  - process_payment_captured()
  - process_payment_failed()
  - process_refund_processed()

### 7.5 — Celery Tasks
- [ ] Create `apps/payments/tasks.py`
  - release_abandoned_stock(order_id) — after 15 min timeout
  - check_pending_payments() — periodic, reconcile with Razorpay

### 7.6 — Views & URLs
- [ ] Create `apps/payments/views.py`
  - PaymentInitiateView (creates Razorpay order, returns data for frontend)
  - PaymentCallbackView (verifies, captures, redirects)
  - PaymentWebhookView (CSRF-exempt, signature-verified)
  - PaymentFailureView
- [ ] Create `apps/payments/urls.py`
- [ ] Wire webhook URL into `config/urls/webhooks.py`

### 7.7 — Frontend Integration
- [ ] Create `static/js/razorpay_checkout.js`
  - Opens Razorpay modal with server-provided data
  - On success: POST to callback URL
  - On failure: redirect to failure page
  - NEVER sends price from frontend

### 7.8 — Templates
- [ ] Create `templates/payments/payment_processing.html`
- [ ] Create `templates/payments/payment_success.html`
- [ ] Create `templates/payments/payment_failure.html`

### 7.9 — Tests
- [ ] Create `apps/payments/tests/factories.py`
- [ ] Create `apps/payments/tests/test_services.py`
  - Payment initiation creates correct Razorpay order
  - Successful verification updates order + payment status
  - Failed verification does not update order
- [ ] Create `apps/payments/tests/test_webhooks.py`
  - Valid signature accepted
  - Invalid/tampered signature rejected
  - Duplicate event_id returns 200 (idempotent, not reprocessed)
  - Amount mismatch detected and logged
- [ ] Create `apps/payments/tests/test_gateway.py`
  - Razorpay gateway creates order correctly
  - Signature verification works
  - Refund initiation works
- [ ] Create `apps/payments/tests/test_security.py`
  - Tampered amount rejected
  - Replayed webhook handled idempotently
  - Double submit prevented
  - CSRF exempt only on webhook endpoint

### 7.10 — Verification
- [ ] `python manage.py check`
- [ ] `pytest apps/payments/tests/ -v`
- [ ] Update CURRENT STATUS
- [ ] WAIT for user go-ahead

---

## STEP 8: Promotions App

**Goal**: Coupons with validation and abuse prevention, homepage banners.

### 8.1 — Models
- [ ] Create `apps/promotions/` boilerplate
- [ ] Create `apps/promotions/models.py` (Coupon, CouponUsage, Banner)
- [ ] Run migrations

### 8.2 — Services
- [ ] Create `apps/promotions/services.py`
  - CouponService:
    - validate_coupon(code, user, cart_total, categories) → CouponResult
    - apply_coupon(order, coupon) → discount amount
    - record_usage(coupon, user, order)
    - Checks: active, date range, usage limits (total + per-user),
      min order value, applicable categories, one per order

### 8.3 — Views, Admin, Templates
- [ ] Views: ApplyCouponView (HTMX), RemoveCouponView
- [ ] Admin: CouponAdmin (usage stats, bulk activate/deactivate), BannerAdmin
- [ ] Templates: coupon input partial, banner display partials

### 8.4 — Tests
- [ ] Valid coupon applied
- [ ] Expired coupon rejected
- [ ] Usage limit exceeded rejected
- [ ] Per-user limit exceeded rejected
- [ ] Min order value not met rejected
- [ ] Category restriction enforced
- [ ] Coupon abuse: same user multiple times

### 8.5 — Verification
- [ ] `python manage.py check`
- [ ] `pytest apps/promotions/tests/ -v`
- [ ] Update CURRENT STATUS
- [ ] WAIT for user go-ahead

---

## STEP 9: Wishlist + Reviews

**Goal**: Wishlist (authenticated users only), reviews with verified-purchase
badge and admin moderation.

### 9.1 — Wishlist
- [ ] Models: WishlistItem (user, product, unique together)
- [ ] Views: WishlistView, AddToWishlistView, RemoveFromWishlistView (HTMX)
- [ ] Templates: wishlist page, wishlist button partial
- [ ] IDOR test: user A cannot see user B's wishlist

### 9.2 — Reviews
- [ ] Models: Review (product, user, rating 1-5, title, body, is_verified_purchase, is_approved)
- [ ] Services: submit_review() — auto-set verified_purchase flag, check if user bought product
- [ ] Views: SubmitReviewView, product detail includes approved reviews
- [ ] Admin: ReviewAdmin (approve/reject, filter by status, verified badge)
- [ ] Templates: review form, review list, star rating display

### 9.3 — Tests
- [ ] Wishlist add/remove
- [ ] Wishlist IDOR
- [ ] Review submission (verified purchase auto-detected)
- [ ] One review per user per product
- [ ] Unapproved reviews not shown publicly
- [ ] Rating constraints (1-5)

### 9.4 — Verification & Handoff

---

## STEP 10: Audit App + Admin Customization + Roles

**Goal**: Centralized audit trail, professional admin panel, role-based access
with management command.

### 10.1 — Audit App
- [ ] Create `apps/audit/` with all files
- [ ] AuditLog model (actor, action, category, target, IP, detail, severity)
- [ ] AuditService.log() — called from services, signals, middleware
- [ ] AuditMiddleware — captures request metadata (IP, user-agent, request-id)
- [ ] Signals: hook into auth events, payment events, order events
- [ ] Admin: read-only AuditLog viewer (filter by category, action, actor, date)

### 10.2 — Role Setup Command
- [ ] Create `apps/core/management/commands/setup_groups.py`
  - Creates groups: content_manager, product_manager, order_manager, admin
  - Assigns exact permissions per role (as defined in permission matrix)
  - Idempotent (safe to run multiple times)

### 10.3 — Admin Customization
- [ ] Custom admin site class (branding: "Elorah Jewelry Administration")
- [ ] Admin URL from env var
- [ ] 2FA for staff (django-otp integration)
- [ ] Admin action logging → AuditLog
- [ ] Custom dashboard (order stats, low stock alerts, recent orders)

### 10.4 — Tests
- [ ] setup_groups creates correct groups and permissions
- [ ] Product Manager can manage products but not orders
- [ ] Order Manager can manage orders but not products
- [ ] Content Manager can manage banners/coupons but not products/orders
- [ ] Admin can do everything except manage staff
- [ ] Non-staff cannot access admin panel
- [ ] 2FA required for staff login

### 10.5 — Verification & Handoff

---

## STEP 11: SEO

**Goal**: Sitemaps, robots.txt, schema.org JSON-LD, meta tags, breadcrumbs,
canonical URLs, Open Graph/Twitter tags.

### 11.1 — Implementation
- [ ] Sitemap framework: ProductSitemap, CategorySitemap, StaticSitemap
- [ ] robots.txt (allow Googlebot, disallow admin/cart/checkout)
- [ ] Schema.org JSON-LD: Product, Offer, AggregateRating, BreadcrumbList, Organization
- [ ] `_seo_meta.html` partial: meta title, description, canonical, OG, Twitter
- [ ] Breadcrumbs on every page
- [ ] Canonical URLs (filter/sort parameters excluded)
- [ ] 301 redirect on slug change (signal-based)

### 11.2 — Tests & Verification

---

## STEP 12: UI Polish / Homepage

**Goal**: Premium Elorah Jewelry homepage, polished product cards, checkout flow,
responsive design, Tailwind compilation, all visual elements.

### 12.1 — Homepage
- [ ] Hero section (premium banner)
- [ ] Featured collections
- [ ] Categories showcase
- [ ] Best sellers
- [ ] New arrivals
- [ ] Promotional banner
- [ ] About the brand
- [ ] Customer reviews/testimonials
- [ ] Trust & security section (secure payments, hallmark, etc.)
- [ ] Newsletter signup
- [ ] Footer (links, social, legal)

### 12.2 — Component Polish
- [ ] Product card (hover image swap, discount badge, wishlist, quick view)
- [ ] Product detail page (gallery, zoom, variants, pricing breakup)
- [ ] Cart page/drawer
- [ ] Checkout flow (multi-step, clean)
- [ ] Account dashboard
- [ ] Empty states, loading states, toast messages
- [ ] Mobile navigation (hamburger menu, bottom nav)
- [ ] Responsive testing (mobile, tablet, desktop)

### 12.3 — Accessibility
- [ ] Semantic HTML throughout
- [ ] Alt text on all images
- [ ] Color contrast (WCAG AA)
- [ ] Keyboard navigation
- [ ] ARIA labels where needed

### 12.4 — Tailwind Build
- [ ] Compile Tailwind CSS (production optimized, purged)
- [ ] Verify all pages styled correctly

### 12.5 — Verification & Handoff

---

## STEP 13: Deployment, Docs, Final QA

**Goal**: Docker prod setup, Nginx, scripts, documentation, security checklist,
final test run, quality gate.

### 13.1 — Docker Production
- [ ] Multi-stage `Dockerfile` (non-root user)
- [ ] `docker-compose.prod.yml` (web, postgres, redis, celery worker, celery beat, nginx)
- [ ] `docker/docker-entrypoint.sh` (wait for DB, migrate, collectstatic)
- [ ] `deploy/gunicorn.conf.py`
- [ ] `deploy/nginx/` (all config files with security headers, rate limiting, SSL)

### 13.2 — Scripts
- [ ] `scripts/deploy.sh` (zero-downtime update)
- [ ] `scripts/backup_db.sh` (with encryption, retention)
- [ ] `scripts/restore_db.sh` (tested)
- [ ] `scripts/rotate_secrets.sh`
- [ ] `scripts/security_audit.sh` (pip-audit + check --deploy)

### 13.3 — CI/CD
- [ ] `.github/workflows/ci.yml` (pytest, check --deploy, pip-audit)
- [ ] `.github/workflows/security.yml` (weekly dep scan)

### 13.4 — Seed Data
- [ ] `apps/core/management/commands/seed_demo.py`
  - Categories, materials, purities, metal rates, GST configs
  - Sample products with placeholder images
  - Sample coupons, banners
  - Refuses to run if DEBUG=False

### 13.5 — Documentation
- [ ] `README.md`
- [ ] `docs/architecture.md`
- [ ] `docs/installation.md`
- [ ] `docs/environment_variables.md`
- [ ] `docs/deployment.md`
- [ ] `docs/payment_setup.md`
- [ ] `docs/security_checklist.md`
- [ ] `docs/admin_roles.md`
- [ ] `docs/gst_configuration.md`
- [ ] `docs/backup_restore.md`
- [ ] `docs/testing.md`
- [ ] `docs/go_live_checklist.md`
- [ ] `docs/troubleshooting.md`
- [ ] `SECURITY.md`

### 13.6 — Final Quality Gate
- [ ] Full test suite passes
- [ ] Coverage report (85%+ on cart, orders, payments, pricing, accounts)
- [ ] `python manage.py check --deploy` — zero warnings
- [ ] No secrets in repo (`git log --all -p | grep -i secret`)
- [ ] No DEBUG=True in production settings
- [ ] HTTPS config verified
- [ ] All security headers present
- [ ] Error pages work (no debug info exposed)
- [ ] Mobile UI verified
- [ ] DB migrations run cleanly on empty database
- [ ] Docker prod build runs successfully
- [ ] Backup + restore tested
- [ ] pip-audit clean
- [ ] IDOR tests all passing
- [ ] Payment flow tested (Razorpay test mode)
- [ ] Webhook flow tested

### 13.7 — Final Summary
- [ ] Deliver completion report to user
- [ ] List any remaining recommendations

---

## Notes for Resuming After Quota Break

1. **Read this file first** — check CURRENT STATUS section
2. **Read Phase 1 plan** for detailed model fields if needed:
   `C:\Users\nandh\.gemini\antigravity\brain\aed3bfa9-acaf-4027-bee4-55bb1ac240c9\phase1_plan.md`
3. **Workspace**: `d:\Jewellary`
4. **Check git log** to see what files exist already
5. **Run tests** for any completed apps to verify they still pass
6. **Continue from the next unchecked sub-task** in the current step
7. **After completing a step**: update CURRENT STATUS, summarize, wait for user approval
