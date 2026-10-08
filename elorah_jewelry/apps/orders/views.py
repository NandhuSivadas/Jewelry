from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "orders/checkout.html")

class PlaceOrderView(LoginRequiredMixin, View):
    def post(self, request):
        # Stub
        return redirect('core:home')
