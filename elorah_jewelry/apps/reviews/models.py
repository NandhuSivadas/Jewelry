from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.mixins import TimestampMixin

class Review(TimestampMixin):
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("product", "user")
        constraints = [
            models.CheckConstraint(
                check=Q(rating__gte=1, rating__lte=5), name="review_rating_1_to_5"
            ),
        ]
        
    def __str__(self):
        return f"{self.rating} stars for {self.product.name} by {self.user.email}"
