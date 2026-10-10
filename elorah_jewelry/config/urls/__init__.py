from django.conf import settings
from django.urls import path, include

urlpatterns = [
    # Public customer-facing URLs
    path("", include("config.urls.public")),
    # Admin panel (secret prefix from env)
    path(f"{settings.ADMIN_URL_PREFIX}/", include("config.urls.internal")),
    # Payment webhooks (secret prefix from env)
    path(f"{settings.WEBHOOK_URL_PREFIX}/", include("config.urls.webhooks")),
]

from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handlers
handler400 = "apps.core.views.error_400"
handler403 = "apps.core.views.error_403"
handler404 = "apps.core.views.error_404"
handler500 = "apps.core.views.error_500"
