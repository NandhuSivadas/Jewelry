from django.db import models
from django.conf import settings
from apps.core.mixins import TimestampMixin

class WishlistItem(TimestampMixin):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "product")
        
    def __str__(self):
        return f"{self.user.email} - {self.product.name}"
