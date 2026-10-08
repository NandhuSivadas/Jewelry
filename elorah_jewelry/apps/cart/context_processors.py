from django.db.models import Sum
from .models import CartItem

def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        count = CartItem.objects.filter(cart__user=request.user).aggregate(total=Sum("quantity"))["total"] or 0
    else:
        session_key = request.session.session_key
        if session_key:
            count = CartItem.objects.filter(cart__session_key=session_key).aggregate(total=Sum("quantity"))["total"] or 0
    return {"cart_item_count": count}
