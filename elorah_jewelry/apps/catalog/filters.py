import django_filters
from django.db.models import F
from .models import Product, Category, Material, Purity

class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.active())
    material = django_filters.ModelChoiceFilter(queryset=Material.objects.filter(is_active=True))
    purity = django_filters.ModelChoiceFilter(queryset=Purity.objects.filter(is_active=True))
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = Product
        fields = ["category", "material", "purity"]

    def filter_in_stock(self, queryset, name, value):
        if value:
            return queryset.filter(stock_records__quantity__gt=F("stock_records__reserved")).distinct()
        return queryset
