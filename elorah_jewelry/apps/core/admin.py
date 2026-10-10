from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline, StackedInline

class ElorahAdminSite(admin.AdminSite):
    site_header = "Elorah Jewelry Administration"
    site_title = "Elorah Admin"
    index_title = "Dashboard"

# We just monkey-patch the default admin site for ease of integration
admin.site.site_header = "Elorah Jewelry Administration"
admin.site.site_title = "Elorah Admin"
admin.site.index_title = "Dashboard"
