from django.urls import path
from .views import ApplyCouponView

app_name = "promotions"
urlpatterns = [
    path("apply/", ApplyCouponView.as_view(), name="apply"),
]
