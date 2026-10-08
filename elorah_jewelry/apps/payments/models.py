import uuid
from django.db import models
from django.db.models import Q

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey("orders.Order", on_delete=models.PROTECT, related_name="payments")

    class Gateway(models.TextChoices):
        RAZORPAY = "RAZORPAY"
        COD = "COD"

    class Status(models.TextChoices):
        CREATED = "CREATED"
        AUTHORIZED = "AUTHORIZED"
        CAPTURED = "CAPTURED"
        FAILED = "FAILED"
        REFUNDED = "REFUNDED"

    gateway = models.CharField(max_length=20, choices=Gateway.choices)
    gateway_order_id = models.CharField(max_length=100, unique=True, null=True)
    gateway_payment_id = models.CharField(max_length=100, unique=True, null=True)
    gateway_signature = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="INR")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    method = models.CharField(max_length=30, blank=True)  # upi, card, netbanking
    refund_id = models.CharField(max_length=100, null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(amount__gt=0), name="payment_amount_positive"),
        ]
        
    def __str__(self):
        return f"Payment {self.id} ({self.status})"

class WebhookEvent(models.Model):
    event_id = models.CharField(max_length=100, unique=True, db_index=True)
    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    is_processed = models.BooleanField(default=False)
    processing_error = models.TextField(blank=True)
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Webhook {self.event_type} ({self.event_id})"
