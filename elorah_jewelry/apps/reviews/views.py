from django.shortcuts import redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .services import ReviewService

class SubmitReviewView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '')
        body = request.POST.get('body', '')
        
        try:
            ReviewService.submit_review(request.user, product_id, rating, title, body)
            messages.success(request, "Your review has been submitted and is pending approval.")
        except ValueError as e:
            messages.error(request, str(e))
            
        return redirect('catalog:product-detail', slug="placeholder") # In real app, redirect to product slug
