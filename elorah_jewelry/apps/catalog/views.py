from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from .models import Category
from .selectors import get_product_list, get_product_detail, search_products
from .filters import ProductFilter

class ProductListView(ListView):
    template_name = "catalog/product_list.html"
    context_object_name = "products"
    paginate_by = 24

    def get_queryset(self):
        qs = get_product_list()
        self.filterset = ProductFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['categories'] = Category.objects.active()
        return context

class CategoryDetailView(ProductListView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'], is_active=True)
        # MPTT get_descendants includes the category itself if include_self=True
        descendants = self.category.get_descendants(include_self=True)
        qs = get_product_list().filter(category__in=descendants)
        self.filterset = ProductFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.category
        return context

class ProductDetailView(DetailView):
    template_name = "catalog/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        return get_product_detail(self.kwargs['slug'])

class ProductSearchView(ProductListView):
    @method_decorator(ratelimit(key='ip', rate='30/m', block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        qs = search_products(query)
        self.filterset = ProductFilter(self.request.GET, queryset=qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
