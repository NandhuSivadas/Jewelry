from django.urls import path, include

from django.contrib.sitemaps.views import sitemap
from apps.catalog.sitemaps import ProductSitemap, CategorySitemap
from django.http import HttpResponse

sitemaps = {
    "products": ProductSitemap,
    "categories": CategorySitemap,
}

def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /cart/",
        "Disallow: /checkout/",
        "Disallow: /accounts/",
        "Disallow: /payments/",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots-txt"),
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
