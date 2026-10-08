from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MetalRate, GSTConfig
from .services import PricingService
from django.core.cache import cache

@receiver(post_save, sender=MetalRate)
@receiver(post_delete, sender=MetalRate)
def clear_metal_rate_cache(sender, instance, **kwargs):
    PricingService.invalidate_rate_cache(instance.material_id, instance.purity_id)

@receiver(post_save, sender=GSTConfig)
@receiver(post_delete, sender=GSTConfig)
def clear_gst_config_cache(sender, instance, **kwargs):
    cache.delete(f"gst_rate:{instance.hsn_code}:{instance.applies_to}")
