from django.db import transaction
from .models import Review
from apps.orders.models import Order, OrderItem

class ReviewService:
    @staticmethod
    def submit_review(user, product_id, rating, title, body) -> Review:
        # Check if already reviewed
        if Review.objects.filter(user=user, product_id=product_id).exists():
            raise ValueError("You have already reviewed this product.")
            
        # Check if verified purchase (has DELIVERED order with this product)
        has_purchased = OrderItem.objects.filter(
            order__user=user,
            order__status=Order.Status.DELIVERED,
            product_id=product_id
        ).exists()
        
        review = Review.objects.create(
            user=user,
            product_id=product_id,
            rating=rating,
            title=title,
            body=body,
            is_verified_purchase=has_purchased,
            is_approved=False
        )
        return review
