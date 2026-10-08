from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, VerifyEmailView, ResendVerificationView,
    PasswordResetView, PasswordResetConfirmView, ProfileView, ProfileUpdateView,
    AddressListView, AddressCreateView, AddressUpdateView, AddressDeleteView,
    SetDefaultAddressView, DashboardView, OrderHistoryView
)

app_name = "accounts"
urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("verify-email/<str:token>/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-verification/", ResendVerificationView.as_view(), name="resend-verify"),
    path("password-reset/", PasswordResetView.as_view(), name="password-reset"),
    path("password-reset/confirm/<str:uidb64>/<str:token>/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="profile-edit"),
    path("addresses/", AddressListView.as_view(), name="address-list"),
    path("addresses/add/", AddressCreateView.as_view(), name="address-add"),
    path("addresses/<int:pk>/edit/", AddressUpdateView.as_view(), name="address-edit"),
    path("addresses/<int:pk>/delete/", AddressDeleteView.as_view(), name="address-delete"),
    path("addresses/<int:pk>/set-default/", SetDefaultAddressView.as_view(), name="address-set-default"),
    path("orders/", OrderHistoryView.as_view(), name="order-history"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
