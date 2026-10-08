from django.db import transaction
from django.utils import timezone
from apps.cart.services import CartService, CartException
from apps.pricing.services import PricingService
from .models import Order, OrderItem, OrderAddressSnapshot
import uuid

class EmptyCart(Exception):
    pass
    
class InsufficientStock(Exception):
    pass

class OrderService:

    @staticmethod
    def generate_order_number() -> str:
        date_str = timezone.now().strftime("%Y%m%d")
        # Simplified for now: in production use Redis INCR for daily sequence
        unique_part = uuid.uuid4().hex[:4].upper()
        return f"JW-{date_str}-{unique_part}"

    @staticmethod
    @transaction.atomic
    def create_order(user, cart, shipping_address_dict: dict, billing_address_dict: dict, payment_method: str, guest_email: str = None) -> Order:
        errors = CartService.validate_cart_for_checkout(cart)
        if errors:
            raise InsufficientStock(" | ".join(errors))
            
        if not cart.items.exists():
            raise EmptyCart("Cart is empty")

        # Snapshot addresses
        shipping_snap = OrderAddressSnapshot.objects.create(**shipping_address_dict)
        billing_snap = OrderAddressSnapshot.objects.create(**billing_address_dict)
        
        order = Order(
            order_number=OrderService.generate_order_number(),
            user=user,
            guest_email=guest_email,
            shipping_address=shipping_snap,
            billing_address=billing_snap,
            payment_method=payment_method,
            subtotal=0,
            grand_total=0
        )
        order.save()
        
        subtotal = 0
        tax_total = 0
        
        for item in cart.items.select_related('product', 'variant').all():
            # In real system: lock stock record with select_for_update, check qty, decrement
            
            breakdown = PricingService.snapshot_for_order(item.product, item.variant, shipping_snap.state)
            line_total = float(breakdown['total']) * item.quantity
            
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                product_name=item.product.name,
                sku=item.product.sku,
                quantity=item.quantity,
                price_snapshot=breakdown,
                line_total=line_total
            )
            
            subtotal += float(breakdown['pre_tax_price']) * item.quantity
            tax_total += float(breakdown['tax_amount']) * item.quantity

        order.subtotal = subtotal
        order.tax_amount = tax_total
        order.grand_total = subtotal + tax_total
        order.save(update_fields=['subtotal', 'tax_amount', 'grand_total'])
        
        CartService.clear_cart(cart)
        
        return order
