from django.urls import path
from .views import CheckoutView, PlaceOrderView

app_name = "orders"
urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("place-order/", PlaceOrderView.as_view(), name="place-order"),
]
