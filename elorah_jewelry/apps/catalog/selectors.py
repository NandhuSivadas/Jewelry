from django.db.models import Prefetch
from .models import Product, ProductVariant

def get_product_list():
    """
    Returns base queryset with related data prefetched for list views.
    """
    return Product.objects.filter(is_active=True).select_related(
        'category', 'material', 'purity'
    ).prefetch_related(
        'images', 'stock_records'
    )

def get_product_detail(slug: str):
    """
    Returns single product with ALL related data in minimal queries.
    """
    return Product.objects.select_related(
        'category', 'material', 'purity'
    ).prefetch_related(
        'images',
        'attributes',
        'variants',
        'variants__stock_records',
        'stock_records'
    ).get(slug=slug, is_active=True)

def get_featured_products(limit: int = 8):
    return get_product_list().filter(is_featured=True)[:limit]

def get_new_arrivals(limit: int = 8):
    return get_product_list().filter(is_new_arrival=True).order_by('-created_at')[:limit]

def get_related_products(product: Product, limit: int = 4):
    return get_product_list().filter(
        category=product.category
    ).exclude(pk=product.pk).order_by('?')[:limit]

def search_products(query: str):
    qs = get_product_list()
    if query:
        qs = qs.filter(name__icontains=query) | qs.filter(sku__icontains=query) | qs.filter(short_description__icontains=query)
    return qs.distinct()
