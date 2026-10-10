from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category
from .filters import ProductFilter

class ProductListView(ListView):
    model = Product
    template_name = "catalog/product_list.html"
    context_object_name = "object_list"
    paginate_by = 12

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True).prefetch_related('images', 'category')
        
        # Sort logic
        sort = self.request.GET.get('sort')
        if sort == 'price_asc':
            qs = qs.order_by('base_price')
        elif sort == 'price_desc':
            qs = qs.order_by('-base_price')
        elif sort == 'newest':
            qs = qs.order_by('-created_at')
            
        # Apply filters
        self.filterset = ProductFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['categories'] = Category.objects.filter(is_active=True)
        return context

class CategoryDetailView(ProductListView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        qs = super().get_queryset().filter(category=self.category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class ProductSearchView(ProductListView):
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        qs = super().get_queryset()
        if query:
            qs = qs.filter(name__icontains=query)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).prefetch_related('images', 'variants', 'attributes')
