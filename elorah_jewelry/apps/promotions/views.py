from django.shortcuts import redirect
from django.views import View
from django.contrib import messages
from .services import CouponService, InvalidCoupon
from apps.cart.services import CartService

class ApplyCouponView(View):
    def post(self, request):
        code = request.POST.get('coupon_code')
        # Here we'd link to the cart and apply it in session, then calculate in cart totals
        # This is a stub for the endpoint
        messages.info(request, f"Coupon {code} functionality to be fully wired up.")
        return redirect('cart:detail')
