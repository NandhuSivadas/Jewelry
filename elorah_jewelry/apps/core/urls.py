from django.urls import path
from .views import (
    HomeView, AboutView, ContactView, health_check, security_txt, legal_page
)

app_name = "core"
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("health/", health_check, name="health-check"),
    path(".well-known/security.txt", security_txt, name="security-txt"),
    path("privacy-policy/", legal_page, {"slug": "privacy"}, name="privacy-policy"),
    path("terms/", legal_page, {"slug": "terms"}, name="terms"),
    path("shipping-policy/", legal_page, {"slug": "shipping"}, name="shipping-policy"),
    path("return-policy/", legal_page, {"slug": "return"}, name="return-policy"),
    path("refund-policy/", legal_page, {"slug": "refund"}, name="refund-policy"),
]
