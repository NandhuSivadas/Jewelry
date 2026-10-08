import razorpay
from django.conf import settings
from .base import PaymentGateway

class RazorpayGateway(PaymentGateway):
    def __init__(self):
        # Allow missing keys in tests
        key_id = getattr(settings, 'RAZORPAY_KEY_ID', 'test_key')
        key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', 'test_secret')
        self.client = razorpay.Client(auth=(key_id, key_secret))

    def create_order(self, order_id, amount_paise, currency="INR", receipt=""):
        return self.client.order.create({
            "amount": amount_paise,
            "currency": currency,
            "receipt": receipt,
            "notes": {"order_id": order_id},
        })

    def verify_payment(self, gateway_order_id, gateway_payment_id, signature):
        try:
            self.client.utility.verify_payment_signature({
                "razorpay_order_id": gateway_order_id,
                "razorpay_payment_id": gateway_payment_id,
                "razorpay_signature": signature,
            })
            return True
        except razorpay.errors.SignatureVerificationError:
            return False

    def verify_webhook_signature(self, payload, signature):
        try:
            webhook_secret = getattr(settings, 'RAZORPAY_WEBHOOK_SECRET', 'test_webhook_secret')
            self.client.utility.verify_webhook_signature(payload, signature, webhook_secret)
            return True
        except razorpay.errors.SignatureVerificationError:
            return False

    def fetch_payment(self, gateway_payment_id: str) -> dict:
        return self.client.payment.fetch(gateway_payment_id)

    def initiate_refund(self, gateway_payment_id: str, amount_paise: int) -> dict:
        return self.client.payment.refund(gateway_payment_id, {"amount": amount_paise})
