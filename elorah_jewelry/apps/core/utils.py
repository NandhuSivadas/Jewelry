import uuid
import os
from decimal import Decimal
from django.utils.text import slugify
from django.utils.http import url_has_allowed_host_and_scheme

def format_inr(amount: Decimal) -> str:
    """Format Decimal as Indian Rupee: ₹1,23,456.00"""
    s, *d = str(amount).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    return f"₹{r}{d[0]}{d[1]}" if d else f"₹{r}"

def generate_safe_filename(original_name: str) -> str:
    """uuid4 + original extension (validated). e.g. 'a1b2c3d4.jpg'"""
    ext = os.path.splitext(original_name)[1].lower()
    return f"{uuid.uuid4().hex}{ext}"

def unique_slugify(value: str, model_class) -> str:
    """Generate unique slug, appending -2, -3 etc. if duplicate"""
    original_slug = slugify(value)
    slug = original_slug
    num = 2
    while model_class.objects.filter(slug=slug).exists():
        slug = f"{original_slug}-{num}"
        num += 1
    return slug

def safe_redirect_url(url: str, allowed_hosts: set) -> str:
    """Validate next param - same-origin only, prevent open redirect"""
    url_is_safe = url_has_allowed_host_and_scheme(
        url=url,
        allowed_hosts=allowed_hosts,
        require_https=True,
    )
    return url if url_is_safe else '/'

def get_client_ip(request) -> str:
    """Extract real IP from X-Forwarded-For or REMOTE_ADDR"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
