from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline, StackedInline
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile, Address

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_email_verified']
    list_filter = ['is_staff', 'is_active', 'is_email_verified']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    ordering = ['email']
    filter_horizontal = []
    
    # Custom fields mapping for UserAdmin
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Address)
