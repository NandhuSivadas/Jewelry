from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.catalog.models import Product, SlugRedirect

@receiver(pre_save, sender=Product)
def track_slug_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            if old_instance.slug and old_instance.slug != instance.slug:
                SlugRedirect.objects.create(old_slug=old_instance.slug, new_slug=instance.slug)
        except Product.DoesNotExist:
            pass
