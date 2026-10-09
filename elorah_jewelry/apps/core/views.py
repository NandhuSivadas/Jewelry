from django.shortcuts import render
from django.views import View
from apps.catalog.models import Product, Category
from apps.promotions.models import Banner

class HomeView(View):
    def get(self, request):
        hero_banners = Banner.objects.filter(position=Banner.Position.HERO, is_active=True).order_by('sort_order')
        promo_banners = Banner.objects.filter(position=Banner.Position.PROMO, is_active=True).order_by('sort_order')
        
        # In a real app we'd have an is_bestseller flag or a query, but here we just take the first few
        best_sellers = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
        new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
        
        # Featured categories (using first 4)
        featured_categories = Category.objects.filter(is_active=True)[:4]

        context = {
            "hero_banners": hero_banners,
            "promo_banner": promo_banners.first(),
            "best_sellers": best_sellers,
            "new_arrivals": new_arrivals,
            "featured_categories": featured_categories,
        }
        return render(request, "core/home.html", context)

def error_400(request, exception):
    return render(request, "400.html", status=400)

def error_403(request, exception):
    return render(request, "403.html", status=403)

def error_404(request, exception):
    return render(request, "404.html", status=404)

def error_500(request):
    return render(request, "500.html", status=500)
