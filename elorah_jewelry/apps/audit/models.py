from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    class Category(models.TextChoices):
        AUTH = "AUTH", "Auth"
        PAYMENT = "PAYMENT", "Payment"
        ORDER = "ORDER", "Order"
        ADMIN = "ADMIN", "Admin"
        SECURITY = "SECURITY", "Security"
        DATA = "DATA", "Data"

    class Severity(models.TextChoices):
        INFO = "INFO", "Info"
        WARNING = "WARNING", "Warning"
        CRITICAL = "CRITICAL", "Critical"

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    actor_email = models.CharField(max_length=255, blank=True)
    action = models.CharField(max_length=50, db_index=True)
    category = models.CharField(max_length=30, choices=Category.choices, db_index=True)
    target_type = models.CharField(max_length=100, blank=True)
    target_id = models.CharField(max_length=50, blank=True)
    target_repr = models.CharField(max_length=200, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=300, blank=True)
    detail = models.JSONField(default=dict, blank=True)
    severity = models.CharField(max_length=10, choices=Severity.choices, default=Severity.INFO)

    class Meta:
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["category", "action"]),
            models.Index(fields=["actor", "timestamp"]),
            models.Index(fields=["-timestamp"]),
        ]

    def __str__(self):
        return f"[{self.category}] {self.action} by {self.actor_email or 'System'} at {self.timestamp}"
