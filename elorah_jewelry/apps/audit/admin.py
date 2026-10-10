from django.contrib import admin
from unfold.admin import ModelAdmin as UnfoldModelAdmin, TabularInline, StackedInline
from .models import AuditLog

class AuditLogAdmin(UnfoldModelAdmin):
    list_display = ["timestamp", "actor_email", "action", "category", "target_repr", "severity", "ip_address"]
    list_filter = ["category", "severity", "action"]
    search_fields = ["actor_email", "target_repr", "ip_address"]
    date_hierarchy = "timestamp"

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(AuditLog, AuditLogAdmin)
