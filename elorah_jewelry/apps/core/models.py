from django.db import models
from django.core.cache import cache

class SiteConfig(models.Model):
    """Singleton - admin-editable store settings. Cached in Redis."""

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    store_name = models.CharField(max_length=200, default="Elorah Jewelry")
    store_email = models.EmailField(blank=True)
    store_phone = models.CharField(max_length=15, blank=True)
    store_gstin = models.CharField(max_length=15, blank=True,
                            help_text="GST Identification Number")
    store_address = models.TextField(blank=True, help_text="Full address for invoices")
    store_state = models.CharField(max_length=100, default="Kerala",
                            help_text="State for CGST/SGST vs IGST")
    store_logo = models.ImageField(upload_to="site/", null=True, blank=True)

    # Business rules (admin-configurable)
    cod_enabled = models.BooleanField(default=True)
    cod_max_amount = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    free_shipping_threshold = models.DecimalField(max_digits=10, decimal_places=2,
                                           default=2000)
    max_qty_per_product = models.PositiveIntegerField(default=5)
    maintenance_mode = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1  # Enforce singleton
        super().save(*args, **kwargs)
        cache.delete("site_config")  # Invalidate cache

    @classmethod
    def get(cls):
        config = cache.get("site_config")
        if config is None:
            config, _ = cls.objects.get_or_create(pk=1)
            cache.set("site_config", config, timeout=3600)
        return config
