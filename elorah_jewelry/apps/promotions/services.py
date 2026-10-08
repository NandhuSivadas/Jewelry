from django.db import transaction
from django.utils import timezone
from decimal import Decimal
from .models import Coupon, CouponUsage
from apps.orders.models import Order

class InvalidCoupon(Exception):
    pass

class CouponService:
    @staticmethod
    def validate_coupon(code: str, user, cart_total: Decimal, cart_categories: list[int]) -> Coupon:
        code = code.upper()
        now = timezone.now()
        
        try:
            coupon = Coupon.objects.get(code=code)
        except Coupon.DoesNotExist:
            raise InvalidCoupon("Invalid coupon code.")
            
        if not coupon.is_active:
            raise InvalidCoupon("Coupon is inactive.")
            
        if coupon.valid_from > now:
            raise InvalidCoupon("Coupon is not yet valid.")
            
        if coupon.valid_to and coupon.valid_to < now:
            raise InvalidCoupon("Coupon has expired.")
            
        if coupon.usage_limit and coupon.times_used >= coupon.usage_limit:
            raise InvalidCoupon("Coupon usage limit reached.")
            
        user_usage = CouponUsage.objects.filter(coupon=coupon, user=user).count()
        if user_usage >= coupon.usage_per_user:
            raise InvalidCoupon("You have already used this coupon the maximum allowed times.")
            
        if cart_total < coupon.min_order_value:
            raise InvalidCoupon(f"Minimum order value for this coupon is {coupon.min_order_value}.")
            
        applicable_categories = list(coupon.applicable_categories.values_list('id', flat=True))
        if applicable_categories:
            if not any(c in applicable_categories for c in cart_categories):
                raise InvalidCoupon("This coupon is not applicable to the items in your cart.")
                
        return coupon

    @staticmethod
    def calculate_discount(coupon: Coupon, subtotal: Decimal) -> Decimal:
        if coupon.discount_type == Coupon.Type.PERCENTAGE:
            discount = subtotal * (coupon.discount_value / Decimal("100"))
            if coupon.max_discount:
                discount = min(discount, coupon.max_discount)
            return discount.quantize(Decimal("0.01"))
        elif coupon.discount_type == Coupon.Type.FIXED:
            return min(coupon.discount_value, subtotal).quantize(Decimal("0.01"))
        return Decimal("0.00")

    @staticmethod
    @transaction.atomic
    def record_usage(coupon: Coupon, user, order: Order) -> None:
        coupon = Coupon.objects.select_for_update().get(pk=coupon.pk)
        
        # Re-check race conditions
        if coupon.usage_limit and coupon.times_used >= coupon.usage_limit:
            raise InvalidCoupon("Coupon usage limit reached.")
            
        CouponUsage.objects.create(coupon=coupon, user=user, order=order)
        coupon.times_used += 1
        coupon.save(update_fields=['times_used'])
