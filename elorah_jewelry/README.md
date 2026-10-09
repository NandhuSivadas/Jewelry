# Elorah Jewelry - E-Commerce Platform

This is a production-ready, highly modular e-commerce platform built with Django for Elorah Jewelry.

## How to Run the Project (Local Development)

### Prerequisites
1. Python 3.12+
2. PostgreSQL (Optional for local if using SQLite, but strongly recommended. The current settings expect PostgreSQL).
3. Redis (Required for caching dynamic prices and Celery task queues).

### Setup Steps
1. **Create and Activate a Virtual Environment:**
   ``bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ``

2. **Install Dependencies:**
   ``bash
   pip install -r requirements/local.txt
   ``
   *(Note: You will need to create equirements/local.txt that includes Django, psycopg2, redis, celery, etc. if not already present)*

3. **Configure Environment Variables:**
   Create a .env file in the root directory and add necessary variables:
   ``env
   DJANGO_SETTINGS_MODULE=config.settings.local
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgres://user:password@localhost:5432/elorah_db
   REDIS_URL=redis://localhost:6379/1
   ``

4. **Run Migrations:**
   ``bash
   python manage.py migrate
   ``

5. **Create a Superuser (Admin):**
   ``bash
   python manage.py createsuperuser
   ``

6. **Initialize Roles & Permissions:**
   Run the custom setup script to configure staff roles (Content Manager, Product Manager, etc.):
   ``bash
   python manage.py setup_groups
   ``

7. **Start the Development Server:**
   ``bash
   python manage.py runserver
   ``
   Visit http://127.0.0.1:8000/ in your browser. Admin panel is at /admin/.


---

## Folder Structure & Architecture

The project follows a modular, app-centric architecture. Instead of monolithic apps, functionality is heavily decoupled to ensure the platform scales gracefully.

`
elorah_jewelry/
├── apps/                 # Contains all custom Django applications
│   ├── accounts/         # Handles Custom User (Email auth), Profiles, and Addresses.
│   ├── audit/            # Security layer. Immutable logging of admin/auth/payment events.
│   ├── cart/             # Cart mechanics, Redis-backed session cart, pricing calculations.
│   ├── catalog/          # Core inventory: Products, Categories, Materials, Purities, Variants.
│   ├── core/             # Project-wide utilities: Base models, mixins, custom middleware.
│   ├── orders/           # Order processing, state machines, and immutable snapshots.
│   ├── payments/         # Payment gateways (Razorpay), webhook processors, verifications.
│   ├── pricing/          # Dynamic pricing engine: Metal rates, GST rules, making charges.
│   ├── promotions/       # Discount engine: Coupons, usage limits, homepage banners.
│   ├── reviews/          # Customer reviews, moderation, verified purchase detection.
│   └── wishlist/         # User wishlist functionality (HTMX powered).
│
├── config/               # Project configuration (replaces standard django project folder)
│   ├── settings/         # Split settings: base.py, local.py, production.py
│   └── urls/             # Split routing: public.py (customer-facing) vs internal.py (APIs/Admin)
│
├── templates/            # Global HTML Templates (Tailwind & Alpine.js powered)
│   ├── catalog/          # Catalog specific templates (Product lists, details)
│   ├── core/             # Base layouts, home page, error pages
│   └── partials/         # Reusable HTML snippets (navbars, footers, SEO meta, HTMX chunks)
│
├── manage.py             # Django's command-line utility for administrative tasks
└── README.md             # This file
`

### Deep Dive: Why is it structured this way?

**1. The pps/ Directory (Modularity):**
Standard Django tutorials teach you to put everything in the root folder. For enterprise apps, this creates a mess. We placed all apps inside an pps/ directory to keep the root clean. Each app has a single responsibility.
- *Example:* Instead of catalog handling both products and prices, catalog only handles what the item *is*. The pricing app handles *what it costs*. This allows you to change how gold is priced globally without ever touching product data.

**2. The config/ Directory (Settings & Routing):**
Settings change based on where the code runs (your laptop vs a production server). We split the settings into ase.py, local.py, and production.py.
- **Why?** It prevents accidental leaks of production database passwords when developing locally, and ensures the production environment has strictly enforced security rules (like CSP headers and HTTPS).

**3. Internal Service Layers (Business Logic):**
If you look inside folders like pps/pricing/ or pps/orders/, you will see files named services.py. 
- **Why?** Django normally puts business logic in "views" (the web handlers) or "models" (the database definition). This makes code impossible to reuse. By using a "Service Layer", we created isolated functions (e.g., PaymentService.initiate_payment()) that can be called by a web browser, a mobile app API, or a background scheduled task seamlessly.

**4. 	emplates/partials/ (HTMX & Reusability):**
We use a component-driven design on the frontend. The partials folder contains pieces of HTML (like _product_card.html). 
- **Why?** First, it ensures if you change the design of a product card, it updates everywhere. Second, it powers HTMX. When a user clicks "Add to Wishlist", instead of refreshing the whole page, the server just sends back the tiny HTML snippet from partials to swap out the button instantly.
