from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .services import CartService, CartException
from .models import CartItem
from apps.catalog.models import Product, ProductVariant

class CartDetailView(View):
    def get(self, request):
        cart = CartService.get_or_create_cart(request)
        totals = CartService.get_cart_totals(cart)
        
        # Determine template based on HTMX request
        template_name = "cart/partials/_cart_content.html" if request.htmx else "cart/detail.html"
        return render(request, template_name, {"cart_totals": totals})

class AddToCartView(View):
    def post(self, request):
        product_id = request.POST.get('product_id')
        variant_id = request.POST.get('variant_id') or None
        quantity = int(request.POST.get('quantity', 1))
        
        cart = CartService.get_or_create_cart(request)
        
        try:
            CartService.add_item(cart, product_id, variant_id, quantity)
            messages.success(request, "Item added to cart.")
        except CartException as e:
            messages.error(request, str(e))
            
        if request.htmx:
            # Re-render cart count for header
            return render(request, "cart/partials/_cart_count.html")
            
        # fallback for non-HTMX
        return redirect('cart:detail')

class UpdateCartItemView(View):
    def post(self, request, item_id):
        quantity = int(request.POST.get('quantity', 1))
        cart = CartService.get_or_create_cart(request)
        
        try:
            CartService.update_quantity(cart, item_id, quantity)
            messages.success(request, "Cart updated.")
        except CartException as e:
            messages.error(request, str(e))
            
        if request.htmx:
            totals = CartService.get_cart_totals(cart)
            return render(request, "cart/partials/_cart_content.html", {"cart_totals": totals})
            
        return redirect('cart:detail')

class RemoveCartItemView(View):
    def post(self, request, item_id):
        cart = CartService.get_or_create_cart(request)
        CartService.remove_item(cart, item_id)
        messages.success(request, "Item removed.")
        
        if request.htmx:
            totals = CartService.get_cart_totals(cart)
            return render(request, "cart/partials/_cart_content.html", {"cart_totals": totals})
            
        return redirect('cart:detail')
