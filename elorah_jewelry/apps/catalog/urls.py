from django.urls import path
from .views import ProductListView, ProductSearchView, CategoryDetailView, ProductDetailView

app_name = "catalog"
urlpatterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("search/", ProductSearchView.as_view(), name="product-search"),
    path("category/<slug:slug>/", CategoryDetailView.as_view(), name="category-detail"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product-detail"),
]
