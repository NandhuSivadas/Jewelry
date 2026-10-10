from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.core.exceptions import ValidationError, PermissionDenied
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django_ratelimit.decorators import ratelimit

from apps.core.utils import safe_redirect_url
from .models import CustomUser, Address
from .services import AccountService
from .forms import (
    RegisterForm, LoginForm, PasswordResetRequestForm, 
    PasswordResetConfirmForm, ProfileUpdateForm, AddressForm
)

class RegisterView(View):
    @method_decorator(ratelimit(key='ip', rate='5/h', method='POST', block=True))
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = AccountService.register_user(
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    phone=form.cleaned_data.get('phone')
                )
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                messages.success(request, "Registration successful! Please verify your email.")
                
                # Safe redirect handling
                next_url = request.POST.get('next', '/')
                return redirect(safe_redirect_url(next_url, allowed_hosts={request.get_host()}))
            except ValidationError as e:
                form.add_error(None, e.message)
        
        return render(request, "accounts/register.html", {"form": form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, "accounts/register.html", {"form": RegisterForm()})

class LoginView(View):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                # Django automatically cycles session key on login for security
                
                # Check verification but allow login
                if not user.is_email_verified:
                    messages.warning(request, "Please verify your email address to access all features.")
                
                next_url = request.POST.get('next', '/')
                return redirect(safe_redirect_url(next_url, allowed_hosts={request.get_host()}))
            else:
                # Same generic message for invalid email or invalid password
                form.add_error(None, "Invalid email or password.")
                
        return render(request, "accounts/login.html", {"form": form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, "accounts/login.html", {"form": LoginForm()})

class LogoutView(LoginRequiredMixin, View):
    # POST only to prevent CSRF logout attacks
    def post(self, request):
        logout(request)
        messages.success(request, "You have been successfully logged out.")
        return redirect('/')

class VerifyEmailView(View):
    def get(self, request, token):
        try:
            AccountService.verify_email(token)
            messages.success(request, "Email verified successfully!")
        except ValidationError as e:
            messages.error(request, e.message)
        return redirect('accounts:login')

class ResendVerificationView(LoginRequiredMixin, View):
    @method_decorator(ratelimit(key='user', rate='3/h', method='POST', block=True))
    def post(self, request):
        if not request.user.is_email_verified:
            AccountService.send_verification_email(request.user)
            messages.success(request, "Verification email sent.")
        return redirect('accounts:profile')

class PasswordResetView(View):
    @method_decorator(ratelimit(key='ip', rate='3/h', method='POST', block=True))
    def post(self, request):
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            AccountService.initiate_password_reset(form.cleaned_data['email'])
            # Always show the same success message to prevent enumeration
            messages.success(request, "If an account exists with this email, a reset link has been sent.")
            return redirect('accounts:login')
        return render(request, "accounts/password_reset.html", {"form": form})
        
    def get(self, request):
        return render(request, "accounts/password_reset.html", {"form": PasswordResetRequestForm()})

class PasswordResetConfirmView(View):
    def post(self, request, uidb64, token):
        # Implementation for token validation and password reset...
        pass
        
    def get(self, request, uidb64, token):
        # ...
        pass

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/profile.html", {
            "user": request.user,
            "profile": request.user.profile,
            "addresses": request.user.addresses.all()
        })

class ProfileUpdateView(LoginRequiredMixin, View):
    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            
            # Also update user fields if present in form
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save(update_fields=['first_name', 'last_name'])
            
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
        return render(request, "accounts/profile_edit.html", {"form": form})

    def get(self, request):
        form = ProfileUpdateForm(instance=request.user.profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name
        })
        return render(request, "accounts/profile_edit.html", {"form": form})

class AddressListView(LoginRequiredMixin, ListView):
    template_name = "accounts/address_list.html"
    context_object_name = "addresses"

    def get_queryset(self):
        # IDOR prevention: Always filter by request.user
        return Address.objects.filter(user=self.request.user)

class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = "accounts/address_form.html"
    success_url = reverse_lazy('accounts:address-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = "accounts/address_form.html"
    success_url = reverse_lazy('accounts:address-list')

    def get_queryset(self):
        # IDOR prevention
        return Address.objects.filter(user=self.request.user)

class AddressDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address = get_object_or_404(Address, pk=pk, user=request.user)
        address.delete()
        messages.success(request, "Address deleted.")
        return redirect('accounts:address-list')

class SetDefaultAddressView(LoginRequiredMixin, View):
    def post(self, request, pk):
        address_type = request.POST.get('type')  # 'shipping' or 'billing'
        try:
            AccountService.set_default_address(request.user, pk, address_type)
            messages.success(request, f"Default {address_type} address updated.")
        except PermissionDenied as e:
            messages.error(request, str(e))
        except ValidationError as e:
            messages.error(request, e.message)
            
        return redirect('accounts:address-list')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/dashboard.html", {})

class OrderHistoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "accounts/order_history.html", {})
