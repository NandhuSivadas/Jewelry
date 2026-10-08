from django.urls import path
from .views import InitiatePaymentView, VerifyPaymentView, RazorpayWebhookView

app_name = "payments"
urlpatterns = [
    path("initiate/<str:order_number>/", InitiatePaymentView.as_view(), name="initiate"),
    path("verify/", VerifyPaymentView.as_view(), name="verify"),
    path("webhook/razorpay/", RazorpayWebhookView.as_view(), name="webhook-razorpay"),
]
