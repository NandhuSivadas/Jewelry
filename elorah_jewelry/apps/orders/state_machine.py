from django.db import transaction
from .models import Order, OrderStatusLog
from django.utils import timezone

VALID_TRANSITIONS = {
    Order.Status.PENDING:          [Order.Status.CONFIRMED, Order.Status.CANCELLED],
    Order.Status.CONFIRMED:        [Order.Status.PROCESSING, Order.Status.CANCELLED],
    Order.Status.PROCESSING:       [Order.Status.SHIPPED, Order.Status.CANCELLED],
    Order.Status.SHIPPED:          [Order.Status.DELIVERED],
    Order.Status.DELIVERED:        [Order.Status.RETURN_REQUESTED],
    Order.Status.RETURN_REQUESTED: [Order.Status.RETURNED, Order.Status.DELIVERED],
    Order.Status.CANCELLED:        [],
    Order.Status.RETURNED:         [],
}

CUSTOMER_ALLOWED_TRANSITIONS = {
    Order.Status.PENDING:   [Order.Status.CANCELLED],
    Order.Status.CONFIRMED: [Order.Status.CANCELLED],
    Order.Status.DELIVERED: [Order.Status.RETURN_REQUESTED],
}

class InvalidStatusTransition(Exception):
    pass

def can_transition(from_status: str, to_status: str, is_admin: bool = False) -> bool:
    if is_admin:
        return to_status in VALID_TRANSITIONS.get(from_status, [])
    return to_status in CUSTOMER_ALLOWED_TRANSITIONS.get(from_status, [])

@transaction.atomic
def transition_order(order: Order, new_status: str, actor, note: str = "") -> Order:
    # Lock the order
    order = Order.objects.select_for_update().get(pk=order.pk)
    old_status = order.status
    
    is_admin = actor.is_staff if actor and hasattr(actor, 'is_staff') else False
    
    if not can_transition(old_status, new_status, is_admin=is_admin):
        raise InvalidStatusTransition(f"Cannot transition from {old_status} to {new_status}")
        
    order.status = new_status
    order.save(update_fields=['status'])
    
    OrderStatusLog.objects.create(
        order=order,
        old_status=old_status,
        new_status=new_status,
        actor=actor,
        note=note
    )
    
    # Side effects could be triggered here via signals or direct calls
    # e.g., if new_status == CANCELLED: release_stock(order)
    
    return order
