from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

ROLE_PERMISSIONS = {
    "content_manager": {
        "promotions": ["add_coupon", "change_coupon", "view_coupon", "add_banner", "change_banner", "delete_banner", "view_banner"],
        "reviews": ["change_review", "view_review"],
    },
    "product_manager": {
        "catalog": ["add_product", "change_product", "view_product", "add_productimage", "change_productimage", "delete_productimage", "add_productvariant", "change_productvariant", "add_category", "change_category", "view_category", "change_stockrecord", "view_stockrecord", "add_material", "change_material", "view_material", "add_purity", "change_purity", "view_purity"],
        "pricing": ["add_metalrate", "change_metalrate", "view_metalrate"],
    },
    "order_manager": {
        "orders": ["view_order", "change_order", "view_orderitem", "view_orderstatuslog"],
        "payments": ["view_payment", "view_webhookevent"],
        "accounts": ["view_customuser", "view_address"],
    },
    "admin": {
        "pricing": ["add_gstconfig", "change_gstconfig", "view_gstconfig", "add_shippingzone", "change_shippingzone", "add_shippingrate", "change_shippingrate", "add_pincodeserviceability", "change_pincodeserviceability"],
        "core": ["change_siteconfig", "view_siteconfig"],
        "audit": ["view_auditlog"],
    },
}

class Command(BaseCommand):
    help = 'Creates default groups and permissions for role-based access control.'

    def handle(self, *args, **options):
        # Accumulate admin permissions
        admin_perms = {}
        for role, apps in ROLE_PERMISSIONS.items():
            if role != "admin":
                for app, perms in apps.items():
                    if app not in admin_perms:
                        admin_perms[app] = []
                    admin_perms[app].extend(perms)
                    
        for app, perms in ROLE_PERMISSIONS["admin"].items():
            if app not in admin_perms:
                admin_perms[app] = []
            admin_perms[app].extend(perms)
            
        ROLE_PERMISSIONS["admin"] = admin_perms

        for role_name, apps in ROLE_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=role_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created group: {role_name}'))
            
            for app_label, perm_codenames in apps.items():
                for codename in perm_codenames:
                    try:
                        perm = Permission.objects.get(content_type__app_label=app_label, codename=codename)
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f'Permission not found: {app_label}.{codename}'))
                        
            self.stdout.write(self.style.SUCCESS(f'Assigned permissions to {role_name}'))
