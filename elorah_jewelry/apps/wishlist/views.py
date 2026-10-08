from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import WishlistItem
from apps.catalog.models import Product

class WishlistView(LoginRequiredMixin, View):
    def get(self, request):
        items = WishlistItem.objects.filter(user=request.user).select_related('product')
        return render(request, "wishlist/list.html", {"items": items})

class AddToWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        WishlistItem.objects.get_or_create(user=request.user, product=product)
        if request.htmx:
            return HttpResponse('<button class="text-red-500">♥ Added</button>')
        return redirect('wishlist:list')

class RemoveFromWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
        if request.htmx:
            return HttpResponse('')
        return redirect('wishlist:list')
