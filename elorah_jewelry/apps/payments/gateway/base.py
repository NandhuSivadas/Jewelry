from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def create_order(self, order_id: str, amount_paise: int, currency: str = "INR", receipt: str = "") -> dict:
        pass

    @abstractmethod
    def verify_payment(self, gateway_order_id: str, gateway_payment_id: str, gateway_signature: str) -> bool:
        pass

    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        pass

    @abstractmethod
    def fetch_payment(self, gateway_payment_id: str) -> dict:
        pass

    @abstractmethod
    def initiate_refund(self, gateway_payment_id: str, amount_paise: int) -> dict:
        pass
