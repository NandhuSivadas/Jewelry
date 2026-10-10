from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline, StackedInline
from .models import MetalRate, GSTConfig, ShippingZone, ShippingRate, PincodeServiceability

class MetalRateAdmin(UnfoldModelAdmin):
    list_display = ["material", "purity", "rate_per_gram", "effective_date", "is_current", "updated_by"]
    list_filter = ["is_current", "material", "purity"]
    search_fields = ["material__name", "purity__name"]
    date_hierarchy = "effective_date"

    def save_model(self, request, obj, form, change):
        if obj.is_current:
            # Set other current rates for this material/purity to False
            MetalRate.objects.filter(
                material=obj.material, 
                purity=obj.purity, 
                is_current=True
            ).exclude(pk=obj.pk).update(is_current=False)
        if not getattr(obj, "updated_by", None):
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class GSTConfigAdmin(UnfoldModelAdmin):
    list_display = ["name", "hsn_code", "tax_rate", "applies_to", "is_active", "effective_from"]
    list_filter = ["is_active", "applies_to"]
    search_fields = ["name", "hsn_code"]

class ShippingRateInline(TabularInline):
    model = ShippingRate
    extra = 1

class PincodeInline(TabularInline):
    model = PincodeServiceability
    extra = 1

class ShippingZoneAdmin(UnfoldModelAdmin):
    list_display = ["name", "is_active"]
    inlines = [ShippingRateInline, PincodeInline]

admin.site.register(MetalRate, MetalRateAdmin)
admin.site.register(GSTConfig, GSTConfigAdmin)
admin.site.register(ShippingZone, ShippingZoneAdmin)
