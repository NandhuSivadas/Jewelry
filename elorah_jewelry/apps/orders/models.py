from django.db import models
from django.db.models import Q
from django.conf import settings
from apps.core.mixins import TimestampMixin

class OrderAddressSnapshot(TimestampMixin):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)

class Order(TimestampMixin):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        PROCESSING = "PROCESSING", "Processing"
        SHIPPED = "SHIPPED", "Shipped"
        DELIVERED = "DELIVERED", "Delivered"
        CANCELLED = "CANCELLED", "Cancelled"
        RETURN_REQUESTED = "RETURN_REQUESTED", "Return Requested"
        RETURNED = "RETURNED", "Returned"

    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        REFUNDED = "REFUNDED", "Refunded"

    order_number = models.CharField(max_length=20, unique=True, db_index=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL, related_name="orders")
    guest_email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    
    shipping_address = models.ForeignKey(OrderAddressSnapshot, on_delete=models.PROTECT, related_name="+")
    billing_address = models.ForeignKey(OrderAddressSnapshot, on_delete=models.PROTECT, related_name="+")
    
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=50, blank=True)
    shipping_charge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_details = models.JSONField(default=dict)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    payment_method = models.CharField(max_length=20, choices=[("ONLINE","Online"), ("COD","Cash on Delivery")])
    notes = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=["order_number"]),
            models.Index(fields=["user", "status"]),
            models.Index(fields=["status", "created_at"]),
        ]
        constraints = [
            models.CheckConstraint(check=Q(subtotal__gte=0), name="order_subtotal_gte_0"),
            models.CheckConstraint(check=Q(grand_total__gte=0), name="order_total_gte_0"),
            models.CheckConstraint(check=Q(discount_amount__gte=0), name="order_discount_gte_0"),
            models.CheckConstraint(check=Q(shipping_charge__gte=0), name="order_shipping_gte_0"),
            models.CheckConstraint(check=Q(tax_amount__gte=0), name="order_tax_gte_0"),
        ]
        
    def __str__(self):
        return f"Order {self.order_number}"

class OrderItem(TimestampMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("catalog.Product", null=True, on_delete=models.SET_NULL)
    variant = models.ForeignKey("catalog.ProductVariant", null=True, blank=True, on_delete=models.SET_NULL)
    
    # Snapshots
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    
    # Financial snapshots
    price_snapshot = models.JSONField()
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

class OrderStatusLog(TimestampMixin):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="status_logs")
    old_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    note = models.TextField(blank=True)
