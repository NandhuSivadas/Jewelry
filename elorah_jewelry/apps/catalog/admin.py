from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline, StackedInline
from .models import (
    Category, Material, Purity, Product, ProductVariant,
    ProductImage, ProductAttribute, StockRecord
)

class CategoryAdmin(UnfoldModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "is_active", "sort_order"]
    list_editable = ["is_active", "sort_order"]

class MaterialAdmin(UnfoldModelAdmin):
    list_display = ["name"]

class PurityAdmin(UnfoldModelAdmin):
    list_display = ["name", "material", "is_active"]

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1

class ProductVariantInline(TabularInline):
    model = ProductVariant
    extra = 0

class ProductAttributeInline(TabularInline):
    model = ProductAttribute
    extra = 1

class StockRecordInline(StackedInline):
    model = StockRecord
    extra = 0

class ProductAdmin(UnfoldModelAdmin):
    list_display = ["name", "sku", "category", "pricing_mode", "is_active", "is_featured"]
    list_filter = ["is_active", "is_featured", "pricing_mode", "category", "material"]
    search_fields = ["name", "sku", "short_description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInline, ProductImageInline, ProductAttributeInline, StockRecordInline]
    
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "slug", "sku", "category", "material", "purity")
        }),
        ("Content", {
            "fields": ("short_description", "description")
        }),
        ("Pricing Configuration", {
            "fields": ("pricing_mode", "base_price", "discount_percentage", "hsn_code")
        }),
        ("Dynamic Pricing Specs", {
            "fields": ("gross_weight", "net_weight", "making_charge_type", "making_charge_value", "stone_charge"),
            "classes": ("collapse",)
        }),
        ("Status", {
            "fields": ("is_active", "is_featured", "is_new_arrival")
        }),
    )

admin.site.register(Category, CategoryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Purity, PurityAdmin)
admin.site.register(Product, ProductAdmin)
