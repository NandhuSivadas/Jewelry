from django.db import models
from django.db.models import Q
from django.conf import settings
from apps.core.mixins import TimestampMixin

class Coupon(TimestampMixin):
    class Type(models.TextChoices):
        PERCENTAGE = "PERCENTAGE", "Percentage"
        FIXED = "FIXED", "Fixed Amount"

    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_type = models.CharField(max_length=20, choices=Type.choices)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField(null=True, blank=True)
    
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    usage_per_user = models.PositiveIntegerField(default=1)
    times_used = models.PositiveIntegerField(default=0)
    
    applicable_categories = models.ManyToManyField("catalog.Category", blank=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(discount_value__gt=0), name="coupon_discount_value_positive"),
            models.CheckConstraint(check=Q(min_order_value__gte=0), name="coupon_min_order_value_gte_0"),
        ]

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code

class CouponUsage(TimestampMixin):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="usages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("coupon", "order")

class Banner(TimestampMixin):
    class Position(models.TextChoices):
        HERO = "HERO", "Main hero slider"
        PROMO = "PROMO", "Promotional strip"
        SIDEBAR = "SIDEBAR", "Sidebar"

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to="banners/")
    image_mobile = models.ImageField(upload_to="banners/mobile/", null=True, blank=True)
    video = models.FileField(upload_to="banners/videos/", null=True, blank=True, help_text="Upload MP4 video for background")
    link_url = models.URLField(blank=True)
    position = models.CharField(max_length=20, choices=Position.choices)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ["sort_order"]
