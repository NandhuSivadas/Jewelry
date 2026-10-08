from django.urls import path, include

urlpatterns = [
    path("", include("apps.core.urls")),
    # Apps urls will be uncommented as they are built
    path("accounts/", include("apps.accounts.urls")),
    path("catalog/", include("apps.catalog.urls")),
    path("cart/", include("apps.cart.urls")),
    path("checkout/", include("apps.orders.urls")),
    path("payments/", include("apps.payments.urls")),
    path("wishlist/", include("apps.wishlist.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("promotions/", include("apps.promotions.urls")),
    # path("pricing/", include("apps.pricing.urls")),
]
