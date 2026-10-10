from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline, StackedInline
from .models import Review

class ReviewAdmin(UnfoldModelAdmin):
    list_display = ["product", "user", "rating", "is_verified_purchase", "is_approved", "created_at"]
    list_filter = ["is_approved", "is_verified_purchase", "rating"]
    actions = ["approve_reviews", "reject_reviews"]
    
    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="Reject selected reviews")
    def reject_reviews(self, request, queryset):
        queryset.update(is_approved=False)

admin.site.register(Review, ReviewAdmin)
