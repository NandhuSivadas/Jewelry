from django.db import models
from django.utils.text import slugify
from .utils import unique_slugify

class TimestampMixin(models.Model):
    """Abstract: created_at + updated_at on every model."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class SlugMixin(models.Model):
    """Abstract: auto-generate slug from name."""
    slug = models.SlugField(max_length=220, unique=True, db_index=True)
    class Meta:
        abstract = True
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self.name, self.__class__)
        super().save(*args, **kwargs)
