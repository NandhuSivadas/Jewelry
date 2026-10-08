from django.db import transaction
from django.conf import settings
from .models import Payment, WebhookEvent
from apps.orders.models import Order
from apps.orders.state_machine import transition_order
from .gateway.factory import GatewayFactory
from decimal import Decimal

class PaymentVerificationError(Exception):
    pass

class PaymentService:
    @staticmethod
    @transaction.atomic
    def initiate_payment(order: Order) -> dict:
        # Lock order
        order = Order.objects.select_for_update().get(pk=order.pk)
        
        if order.status != Order.Status.PENDING or order.payment_status != Order.PaymentStatus.PENDING:
            raise ValueError("Order is not in valid state for payment")
            
        amount_paise = int(order.grand_total * 100)
        gateway = GatewayFactory.get_gateway("RAZORPAY")
        
        razorpay_order = gateway.create_order(
            order_id=str(order.id),
            amount_paise=amount_paise,
            receipt=order.order_number
        )
        
        Payment.objects.create(
            order=order,
            gateway=Payment.Gateway.RAZORPAY,
            gateway_order_id=razorpay_order['id'],
            amount=order.grand_total,
            status=Payment.Status.CREATED
        )
        
        return {
            'razorpay_key_id': getattr(settings, 'RAZORPAY_KEY_ID', ''),
            'razorpay_order_id': razorpay_order['id'],
            'amount': amount_paise,
            'currency': 'INR',
            'order_number': order.order_number,
        }

    @staticmethod
    @transaction.atomic
    def verify_and_capture(gateway_order_id: str, gateway_payment_id: str, signature: str) -> Payment:
        payment = Payment.objects.select_for_update().get(gateway_order_id=gateway_order_id)
        
        if payment.status in [Payment.Status.CAPTURED, Payment.Status.AUTHORIZED]:
            return payment
            
        gateway = GatewayFactory.get_gateway(payment.gateway)
        is_valid = gateway.verify_payment(gateway_order_id, gateway_payment_id, signature)
        
        if not is_valid:
            payment.status = Payment.Status.FAILED
            payment.save(update_fields=['status'])
            
            # Update order
            order = payment.order
            order.payment_status = Order.PaymentStatus.FAILED
            order.save(update_fields=['payment_status'])
            raise PaymentVerificationError("Invalid signature")
            
        payment.status = Payment.Status.CAPTURED
        payment.gateway_payment_id = gateway_payment_id
        payment.gateway_signature = signature
        payment.save(update_fields=['status', 'gateway_payment_id', 'gateway_signature'])
        
        # Update order status to CONFIRMED
        order = payment.order
        order.payment_status = Order.PaymentStatus.PAID
        order.save(update_fields=['payment_status'])
        
        # Admin action (System) transitioning
        transition_order(order, Order.Status.CONFIRMED, actor=None, note="Payment verified successfully.")
        
        return payment

    @staticmethod
    def process_webhook(payload: bytes, signature: str) -> None:
        gateway = GatewayFactory.get_gateway("RAZORPAY")
        if not gateway.verify_webhook_signature(payload, signature):
            raise PaymentVerificationError("Webhook signature mismatch")
            
        import json
        data = json.loads(payload.decode('utf-8'))
        event_id = data.get('id')
        event_type = data.get('event')
        
        webhook, created = WebhookEvent.objects.get_or_create(
            event_id=event_id,
            defaults={'event_type': event_type, 'payload': data}
        )
        if not created and webhook.is_processed:
            return
            
        try:
            # E.g. Handle payment.captured, payment.failed
            if event_type == "payment.captured":
                payment_id = data['payload']['payment']['entity']['id']
                order_id = data['payload']['payment']['entity']['order_id']
                # Implement reconciliation logic here...
            
            webhook.is_processed = True
            from django.utils import timezone
            webhook.processed_at = timezone.now()
        except Exception as e:
            webhook.processing_error = str(e)
        finally:
            webhook.save()
