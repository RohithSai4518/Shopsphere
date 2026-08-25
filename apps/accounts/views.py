from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Address, UserPreference, SavedPaymentMethod
from .services import AccountsService
from apps.sellers.services import SellerService
from apps.notifications.models import Notification

def register_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        register_as_seller = request.POST.get('is_seller') == 'on'
        business_name = request.POST.get('business_name', '').strip()

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email address already exists.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            role='SELLER' if register_as_seller else 'CUSTOMER'
        )
        UserPreference.objects.get_or_create(user=user)

        if register_as_seller and business_name:
            SellerService.register_seller(user, business_name, email)

        login(request, user)
        messages.success(request, f"Welcome to ShopSphere, {first_name}!")
        return redirect('catalog:home')

    return render(request, 'accounts/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('catalog:home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        user = authenticate(request, username=email, password=password)

        if user:
            login(request, user)
            AccountsService.create_user_session(user, request.META.get('REMOTE_ADDR'), request.META.get('HTTP_USER_AGENT'))
            messages.success(request, f"Welcome back, {user.first_name}!")
            next_url = request.GET.get('next', 'catalog:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')

def logout_view(request):
    if request.user.is_authenticated:
        AccountsService.invalidate_user_sessions(request.user)
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('catalog:home')

@login_required
def profile_view(request):
    addresses = request.user.addresses.all()
    preference, _ = UserPreference.objects.get_or_create(user=request.user)
    saved_payments = request.user.saved_payment_methods.all()
    recent_notifications = Notification.objects.filter(user=request.user)[:5]

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        phone = request.POST.get('phone', '').strip()

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.phone = phone
        request.user.save()

        preference.email_notifications = request.POST.get('email_notifications') == 'on'
        preference.theme = request.POST.get('theme', 'DARK')
        preference.currency = request.POST.get('currency', 'USD')
        preference.save()

        messages.success(request, 'Profile and preferences updated.')

    return render(request, 'accounts/profile.html', {
        'addresses': addresses,
        'preference': preference,
        'saved_payments': saved_payments,
        'notifications': recent_notifications
    })

@login_required
def add_address_view(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            address_type=request.POST.get('address_type', 'SHIPPING'),
            full_name=request.POST.get('full_name', ''),
            street_address_1=request.POST.get('street_address_1', ''),
            street_address_2=request.POST.get('street_address_2', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            postal_code=request.POST.get('postal_code', ''),
            country=request.POST.get('country', 'United States'),
            is_default=request.POST.get('is_default') == 'on'
        )
        messages.success(request, 'Address saved successfully.')
    return redirect('accounts:profile')

@login_required
def delete_address_view(request, address_id):
    Address.objects.filter(id=address_id, user=request.user).delete()
    messages.info(request, 'Address removed.')
    return redirect('accounts:profile')
