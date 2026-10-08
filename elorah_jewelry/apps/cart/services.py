from dataclasses import dataclass, field
from decimal import Decimal
from django.db.models import Sum
from .models import Cart, CartItem
from apps.catalog.models import Product, ProductVariant
from apps.pricing.services import PricingService, PriceBreakdown
from apps.core.models import SiteConfig

class CartException(Exception):
    pass

class ProductNotAvailable(CartException):
    pass

class InsufficientStock(CartException):
    pass

class MaxQuantityExceeded(CartException):
    pass

class CartItemNotFound(CartException):
    pass

@dataclass
class CartItemTotals:
    item: CartItem
    breakdown: PriceBreakdown
    line_total: Decimal

@dataclass
class CartTotals:
    items: list[CartItemTotals] = field(default_factory=list)
    subtotal: Decimal = Decimal("0.00")
    tax_total: Decimal = Decimal("0.00")
    grand_total: Decimal = Decimal("0.00")
    item_count: int = 0

class CartService:

    @staticmethod
    def get_or_create_cart(request) -> Cart:
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            return cart
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, _ = Cart.objects.get_or_create(session_key=session_key)
            return cart

    @staticmethod
    def _validate_stock(product: Product, variant: ProductVariant, requested_quantity: int) -> None:
        if not product.is_active:
            raise ProductNotAvailable("Product is not available.")
        
        # Get stock record
        stock_record = None
        if variant:
            stock_record = variant.stock_records.first()
        else:
            stock_record = product.stock_records.filter(variant__isnull=True).first()
            
        if not stock_record or stock_record.available < requested_quantity:
            raise InsufficientStock("Insufficient stock available.")
            
        max_qty = SiteConfig.get().max_qty_per_product
        if requested_quantity > max_qty:
            raise MaxQuantityExceeded(f"Cannot order more than {max_qty} units of a single product.")

    @staticmethod
    def add_item(cart: Cart, product_id: int, variant_id: int = None, quantity: int = 1) -> CartItem:
        if quantity < 1:
            raise ValueError("Quantity must be at least 1")
            
        try:
            product = Product.objects.get(id=product_id, is_active=True)
            variant = ProductVariant.objects.get(id=variant_id, product=product) if variant_id else None
        except (Product.DoesNotExist, ProductVariant.DoesNotExist):
            raise ProductNotAvailable("Product or variant not found.")

        # Check existing item to sum requested qty
        existing_item = CartItem.objects.filter(cart=cart, product=product, variant=variant).first()
        total_requested = (existing_item.quantity + quantity) if existing_item else quantity
        
        CartService._validate_stock(product, variant, total_requested)

        if existing_item:
            existing_item.quantity = total_requested
            existing_item.save(update_fields=['quantity'])
            return existing_item
        else:
            return CartItem.objects.create(
                cart=cart,
                product=product,
                variant=variant,
                quantity=quantity
            )

    @staticmethod
    def update_quantity(cart: Cart, item_id: int, quantity: int) -> CartItem:
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            raise CartItemNotFound("Item not found in your cart.")
            
        if quantity <= 0:
            item.delete()
            return None
            
        CartService._validate_stock(item.product, item.variant, quantity)
        item.quantity = quantity
        item.save(update_fields=['quantity'])
        return item

    @staticmethod
    def remove_item(cart: Cart, item_id: int) -> None:
        CartItem.objects.filter(id=item_id, cart=cart).delete()

    @staticmethod
    def merge_carts(session_cart: Cart, user_cart: Cart) -> Cart:
        for session_item in session_cart.items.all():
            user_item = CartItem.objects.filter(
                cart=user_cart, 
                product=session_item.product, 
                variant=session_item.variant
            ).first()
            
            if user_item:
                if session_item.quantity > user_item.quantity:
                    user_item.quantity = session_item.quantity
                    user_item.save(update_fields=['quantity'])
            else:
                session_item.cart = user_cart
                session_item.save(update_fields=['cart'])
                
        session_cart.delete()
        return user_cart

    @staticmethod
    def get_cart_totals(cart: Cart) -> CartTotals:
        items = list(cart.items.select_related('product', 'product__material', 'product__purity', 'variant').all())
        totals = CartTotals()
        
        for item in items:
            try:
                # No buyer_state here yet, assumed intra-state for cart preview or we can pass it if we have default address
                breakdown = PricingService.compute_price(item.product, item.variant)
                line_total = breakdown.total * item.quantity
                
                totals.items.append(CartItemTotals(
                    item=item,
                    breakdown=breakdown,
                    line_total=line_total
                ))
                
                totals.subtotal += (breakdown.pre_tax_price * item.quantity)
                totals.tax_total += (breakdown.tax_amount * item.quantity)
                totals.grand_total += line_total
                totals.item_count += item.quantity
            except Exception:
                # If price calculation fails (e.g. rate missing), skip or handle gracefully
                pass
                
        return totals

    @staticmethod
    def validate_cart_for_checkout(cart: Cart) -> list[str]:
        errors = []
        items = cart.items.select_related('product', 'variant').all()
        
        if not items:
            errors.append("Your cart is empty.")
            return errors
            
        for item in items:
            if not item.product.is_active:
                errors.append(f"{item.product.name} is no longer available.")
                continue
                
            try:
                CartService._validate_stock(item.product, item.variant, item.quantity)
            except CartException as e:
                errors.append(f"Issue with {item.product.name}: {str(e)}")
                
        return errors

    @staticmethod
    def clear_cart(cart: Cart) -> None:
        cart.items.all().delete()
