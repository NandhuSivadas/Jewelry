from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from .models import Coupon, CouponUsage, Banner

class CouponAdmin(UnfoldModelAdmin):
    list_display = ["code", "discount_type", "discount_value", "is_active", "valid_to"]
    list_filter = ["is_active", "discount_type"]
    search_fields = ["code"]
    filter_horizontal = ["applicable_categories"]

class CouponUsageAdmin(UnfoldModelAdmin):
    list_display = ["coupon", "user", "order", "created_at"]
    
class BannerAdmin(UnfoldModelAdmin):
    list_display = ["title", "position", "is_active", "sort_order"]
    list_filter = ["position", "is_active"]
    search_fields = ["title"]
    list_editable = ["sort_order", "is_active"]

admin.site.register(Coupon, CouponAdmin)
admin.site.register(CouponUsage, CouponUsageAdmin)
admin.site.register(Banner, BannerAdmin)
