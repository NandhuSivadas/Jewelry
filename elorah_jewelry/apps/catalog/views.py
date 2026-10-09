from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Product, Category, SlugRedirect
from .filters import ProductFilter

class ProductDetailView(View):
    def get(self, request, slug):
        try:
            product = Product.objects.select_related('category', 'material', 'purity').get(slug=slug, is_active=True)
            return render(request, "catalog/product_detail.html", {"product": product})
        except Product.DoesNotExist:
            redirect_obj = SlugRedirect.objects.filter(old_slug=slug).order_by('-created_at').first()
            if redirect_obj:
                return redirect('catalog:product-detail', slug=redirect_obj.new_slug, permanent=True)
            return render(request, "404.html", status=404)

class ProductListView(View):
    def get(self, request):
        f = ProductFilter(request.GET, queryset=Product.objects.filter(is_active=True))
        return render(request, "catalog/product_list.html", {"products": f.qs, "filterset": f})

class ProductSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '')
        products = Product.objects.filter(name__icontains=query, is_active=True) if query else Product.objects.none()
        return render(request, "catalog/product_list.html", {"products": products, "search_query": query})

class CategoryDetailView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug, is_active=True)
        products = Product.objects.filter(category=category, is_active=True)
        return render(request, "catalog/product_list.html", {"products": products, "current_category": category})
