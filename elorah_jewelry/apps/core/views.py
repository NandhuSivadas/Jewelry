from django.shortcuts import render
from django.views import View
from apps.catalog.models import Product, Category
from apps.promotions.models import Banner

class HomeView(View):
    def get(self, request):
        hero_banners = Banner.objects.filter(position=Banner.Position.HERO, is_active=True).order_by('sort_order')
        
        # Base active products
        active_products = Product.objects.filter(is_active=True)
        
        # 5. Latest Collections (New Arrivals)
        new_arrivals = active_products.filter(is_new_arrival=True).order_by('-created_at')[:6]
        if not new_arrivals.exists():
            new_arrivals = active_products.order_by('-created_at')[:6]
            
        # 6. Flat 15% Off (discount_percentage >= 15)
        discounted_products = active_products.filter(discount_percentage__gte=15).order_by('-discount_percentage')[:6]
        if not discounted_products.exists():
            discounted_products = active_products.filter(discount_percentage__gt=0).order_by('-discount_percentage')[:6]
            
        # 7. Most Loved (Bestsellers or high rating - placeholders for now if none)
        most_loved = active_products.filter(is_featured=True)[:8]
        if not most_loved.exists():
            most_loved = active_products[:8]
            
        # 8. Our Collections Grid (Categories with counts)
        # We need categories that have products
        categories = Category.objects.filter(is_active=True)
        # Since we can't do complex annotations easily without setup, we just pass categories.
        
        # 13. Traditional Necklaces
        necklaces = active_products.filter(category__slug__icontains='necklace')[:6]
        if not necklaces.exists():
            necklaces = active_products[:6]

        context = {
            "hero_banners": hero_banners,
            "new_arrivals": new_arrivals,
            "discounted_products": discounted_products,
            "most_loved": most_loved,
            "categories": categories,
            "necklaces": necklaces,
        }
        return render(request, "core/home.html", context)

def error_400(request, exception):
    return render(request, 'errors/400.html', status=400)

def error_403(request, exception):
    return render(request, 'errors/403.html', status=403)

def error_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def error_500(request):
    return render(request, 'errors/500.html', status=500)
