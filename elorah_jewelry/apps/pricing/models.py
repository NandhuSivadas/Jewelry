from django.db import models
from django.db.models import Q
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.mixins import TimestampMixin
from decimal import Decimal

class MetalRate(TimestampMixin):
    material = models.ForeignKey("catalog.Material", on_delete=models.PROTECT, related_name="metal_rates")
    purity = models.ForeignKey("catalog.Purity", on_delete=models.PROTECT, related_name="metal_rates")
    rate_per_gram = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    effective_date = models.DateField(db_index=True)
    is_current = models.BooleanField(default=True, db_index=True)
    source = models.CharField(max_length=50, default="manual")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("material", "purity", "effective_date")
        constraints = [
            models.CheckConstraint(check=Q(rate_per_gram__gt=0), name="rate_per_gram_positive"),
        ]

    def __str__(self):
        return f"{self.material.name} {self.purity.name} @ {self.rate_per_gram}/g on {self.effective_date}"

class GSTConfig(TimestampMixin):
    class AppliesTo(models.TextChoices):
        TOTAL = "TOTAL", "Total Price"
        METAL = "METAL", "Metal Value Only"
        MAKING = "MAKING", "Making Charges Only"
        STONE = "STONE", "Stone Charges Only"

    name = models.CharField(max_length=100)
    hsn_code = models.CharField(max_length=8, db_index=True)
    description = models.TextField(blank=True)
    tax_rate = models.DecimalField(
        max_digits=5, decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    applies_to = models.CharField(
        max_length=20, choices=AppliesTo.choices, default=AppliesTo.TOTAL
    )
    is_active = models.BooleanField(default=True)
    effective_from = models.DateField()
    effective_to = models.DateField(null=True, blank=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("hsn_code", "applies_to", "effective_from")
        verbose_name = "GST Configuration"

    def __str__(self):
        return f"{self.hsn_code} - {self.tax_rate}%"

class ShippingZone(TimestampMixin):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ShippingRate(TimestampMixin):
    zone = models.ForeignKey(ShippingZone, on_delete=models.CASCADE, related_name="rates")
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.zone.name}: {self.rate}"

class PincodeServiceability(TimestampMixin):
    pincode = models.CharField(max_length=6, unique=True)
    zone = models.ForeignKey(ShippingZone, on_delete=models.PROTECT, related_name="pincodes")
    is_cod_available = models.BooleanField(default=True)
    is_delivery_available = models.BooleanField(default=True)
    estimated_days = models.PositiveIntegerField(default=5)
    
    def __str__(self):
        return self.pincode
