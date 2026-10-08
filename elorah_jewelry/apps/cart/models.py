from django.db import models
from django.db.models import Q
from django.conf import settings
from apps.core.mixins import TimestampMixin

class Cart(TimestampMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="cart")
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(Q(user__isnull=False) | Q(session_key__isnull=False)),
                name="cart_has_user_or_session"
            ),
        ]
        
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.email}"
        return f"Guest Cart ({self.session_key})"

class CartItem(TimestampMixin):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    variant = models.ForeignKey("catalog.ProductVariant", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("cart", "product", "variant")
        constraints = [
            models.CheckConstraint(
                check=Q(quantity__gte=1), name="cart_item_qty_min_1"
            ),
        ]
        
    def __str__(self):
        v_name = f" ({self.variant.size})" if self.variant else ""
        return f"{self.quantity} x {self.product.name}{v_name}"
