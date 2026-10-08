from .base import PaymentGateway
from .razorpay import RazorpayGateway

class GatewayFactory:
    _gateways = {"RAZORPAY": RazorpayGateway}

    @classmethod
    def get_gateway(cls, name: str = "RAZORPAY") -> PaymentGateway:
        gateway_class = cls._gateways.get(name)
        if not gateway_class:
            raise ValueError(f"Unknown gateway: {name}")
        return gateway_class()

    @classmethod
    def register(cls, name: str, gateway_class: type):
        cls._gateways[name] = gateway_class
