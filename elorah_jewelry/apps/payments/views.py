from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import PaymentService, PaymentVerificationError
from apps.orders.models import Order
import logging

logger = logging.getLogger(__name__)

class InitiatePaymentView(View):
    def post(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
        try:
            payment_data = PaymentService.initiate_payment(order)
            return JsonResponse(payment_data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

class VerifyPaymentView(View):
    def post(self, request):
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')
        
        try:
            payment = PaymentService.verify_and_capture(razorpay_order_id, razorpay_payment_id, razorpay_signature)
            return redirect('orders:order-success', order_number=payment.order.order_number)
        except PaymentVerificationError:
            return redirect('orders:checkout-review') # Redirect to error page in real app

@method_decorator(csrf_exempt, name='dispatch')
class RazorpayWebhookView(View):
    def post(self, request):
        signature = request.headers.get('X-Razorpay-Signature')
        if not signature:
            return HttpResponse(status=400)
            
        try:
            PaymentService.process_webhook(request.body, signature)
            return HttpResponse(status=200)
        except PaymentVerificationError:
            return HttpResponse(status=400)
        except Exception as e:
            logger.error(f"Webhook error: {str(e)}")
            return HttpResponse(status=500)
