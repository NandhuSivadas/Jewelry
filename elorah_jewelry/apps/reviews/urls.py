from django.urls import path
from .views import SubmitReviewView

app_name = "reviews"
urlpatterns = [
    path("submit/<int:product_id>/", SubmitReviewView.as_view(), name="submit"),
]
