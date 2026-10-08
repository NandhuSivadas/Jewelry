from django.utils import timezone
from .models import SiteConfig

def site_config(request):
    return {
        "site_config": SiteConfig.get(),
        "current_year": timezone.now().year,
    }
