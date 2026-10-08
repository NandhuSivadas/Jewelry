from django.db import models
from django.db.models import Q, F
from mptt.models import MPTTModel, TreeForeignKey
from apps.core.mixins import TimestampMixin, SlugMixin

class CategoryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

class Category(MPTTModel, TimestampMixin):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", null=True, blank=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    sort_order = models.PositiveIntegerField(default=0)

    objects = CategoryQuerySet.as_manager()

    class MPTTMeta:
        order_insertion_by = ["sort_order", "name"]

    def __str__(self):
        return self.name

class Material(TimestampMixin):
    name = models.CharField(max_length=50, unique=True)  # e.g., Gold, Silver, Platinum
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Purity(TimestampMixin):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name="purities")
    name = models.CharField(max_length=50)  # e.g., 22K, 18K, 925
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ("material", "name")
        verbose_name_plural = "purities"

    def __str__(self):
        return f"{self.name} {self.material.name}"

class Product(TimestampMixin, SlugMixin):
    class PricingMode(models.TextChoices):
        FIXED = "FIXED", "Fixed Price"
        DYNAMIC = "DYNAMIC", "Dynamic (Rate * Weight + Charges)"

    class MakingChargeType(models.TextChoices):
        FIXED = "FIXED", "Fixed Amount"
        PER_GRAM = "PER_GRAM", "Per Gram"
        PERCENTAGE = "PERCENTAGE", "Percentage of Metal Value"

    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    
    material = models.ForeignKey(Material, on_delete=models.PROTECT, related_name="products")
    purity = models.ForeignKey(Purity, on_delete=models.PROTECT, related_name="products")

    short_description = models.TextField(max_length=500, blank=True)
    description = models.TextField(blank=True)

    pricing_mode = models.CharField(max_length=10, choices=PricingMode.choices, default=PricingMode.DYNAMIC)
    
    # FIXED mode fields
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # DYNAMIC mode fields
    gross_weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, help_text="In grams")
    net_weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True, help_text="In grams")
    making_charge_type = models.CharField(max_length=15, choices=MakingChargeType.choices, default=MakingChargeType.PER_GRAM)
    making_charge_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stone_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # General properties
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    hsn_code = models.CharField(max_length=20, blank=True)

    is_active = models.BooleanField(default=True, db_index=True)
    is_featured = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["is_active", "category"]),
            models.Index(fields=["is_active", "is_featured"]),
            models.Index(fields=["is_active", "created_at"]),
            models.Index(fields=["material", "purity"]),
            models.Index(fields=["base_price"]),
        ]
        constraints = [
            models.CheckConstraint(check=Q(base_price__gte=0), name="product_base_price_non_negative"),
            models.CheckConstraint(check=Q(gross_weight__gte=0) | Q(gross_weight__isnull=True), name="product_gross_weight_non_negative"),
            models.CheckConstraint(check=Q(net_weight__gte=0) | Q(net_weight__isnull=True), name="product_net_weight_non_negative"),
            models.CheckConstraint(check=Q(discount_percentage__gte=0, discount_percentage__lte=100), name="product_discount_percentage_range"),
            models.CheckConstraint(check=Q(making_charge_value__gte=0), name="product_making_charge_non_negative"),
            models.CheckConstraint(check=Q(stone_charge__gte=0), name="product_stone_charge_non_negative"),
        ]

    def __str__(self):
        return f"[{self.sku}] {self.name}"

class ProductVariant(TimestampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=50, unique=True)
    size = models.CharField(max_length=50) # e.g. Ring size 14, Chain 18 inch
    weight_adjustment = models.DecimalField(max_digits=8, decimal_places=3, default=0)
    price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.product.name} - {self.size}"

class ProductImage(TimestampMixin):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/originals/")
    thumbnail = models.ImageField(upload_to="products/thumbnails/", null=True, blank=True)
    webp_image = models.ImageField(upload_to="products/webp/", null=True, blank=True)
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order"]

class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attributes")
    name = models.CharField(max_length=100) # e.g. "Gemstone", "Cut"
    value = models.CharField(max_length=100) # e.g. "Diamond", "Round Brilliant"

    class Meta:
        unique_together = ("product", "name")

class StockRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_records")
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True, related_name="stock_records")
    quantity = models.PositiveIntegerField(default=0)
    reserved = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "variant")
        constraints = [
            models.CheckConstraint(check=Q(reserved__lte=F("quantity")), name="stock_reserved_lte_quantity"),
        ]

    @property
    def available(self) -> int:
        return self.quantity - self.reserved
