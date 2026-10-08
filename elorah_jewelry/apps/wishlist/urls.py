from django.urls import path
from .views import WishlistView, AddToWishlistView, RemoveFromWishlistView

app_name = "wishlist"
urlpatterns = [
    path("", WishlistView.as_view(), name="list"),
    path("add/<int:product_id>/", AddToWishlistView.as_view(), name="add"),
    path("remove/<int:product_id>/", RemoveFromWishlistView.as_view(), name="remove"),
]
