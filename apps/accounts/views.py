import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .models import User, Address, UserPreference, SavedPaymentMethod, UserTwoFactor, AccountDeletionRequest
from .services import AccountsService
from .security import TOTPService, PasswordResetService
from .privacy import PrivacyService
from apps.sellers.services import SellerService
from apps.notifications.models import Notification
from apps.audit.models import SecurityAuditLog

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
            # Check if user has 2FA enabled
            two_factor = getattr(user, 'two_factor', None)
            if two_factor and two_factor.is_enabled:
                # Store pending authentication user ID in session
                request.session['pending_2fa_user_id'] = user.id
                request.session['pending_2fa_remember'] = request.POST.get('remember_me') == 'on'
                request.session['next_url'] = request.GET.get('next', 'catalog:home')
                return redirect('accounts:two_factor_verify')

            login(request, user)
            AccountsService.create_user_session(user, request.META.get('REMOTE_ADDR'), request.META.get('HTTP_USER_AGENT'))
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'catalog:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')


def two_factor_verify_view(request):
    """
    Second-factor challenge verification during login.
    Accepts standard 6-digit TOTP code or emergency backup code.
    """
    user_id = request.session.get('pending_2fa_user_id')
    if not user_id:
        return redirect('accounts:login')

    user = get_object_or_404(User, id=user_id)
    two_factor = getattr(user, 'two_factor', None)
    if not two_factor or not two_factor.is_enabled:
        return redirect('accounts:login')

    if request.method == 'POST':
        code = request.POST.get('code', '').strip().replace(' ', '')
        is_backup = request.POST.get('is_backup') == '1'

        verified = False
        if is_backup:
            if TOTPService.verify_and_consume_backup_code(two_factor, code):
                verified = True
                messages.warning(request, 'Used one-time emergency backup recovery code. Please generate new backup codes.')
        else:
            if TOTPService.verify_totp(two_factor.secret_key, code):
                verified = True

        if verified:
            # Complete login
            login(request, user)
            request.session.pop('pending_2fa_user_id', None)
            next_url = request.session.pop('next_url', 'catalog:home')
            AccountsService.create_user_session(user, request.META.get('REMOTE_ADDR'), request.META.get('HTTP_USER_AGENT'))
            messages.success(request, f"Two-Factor Authentication verified. Welcome back, {user.first_name}!")
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid authentication code. Please check your authenticator app or backup code.')

    return render(request, 'accounts/two_factor_verify.html', {'user_email': user.email})


@login_required
def two_factor_setup_view(request):
    """
    Setup or manage Two-Factor Authentication.
    Generates a secret key, URI, and 8 one-time backup codes.
    """
    two_factor, _ = UserTwoFactor.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'initiate':
            secret = TOTPService.generate_secret()
            backup_codes = TOTPService.generate_backup_codes(8)
            request.session['setup_2fa_secret'] = secret
            request.session['setup_2fa_backup_codes'] = backup_codes
            uri = TOTPService.get_provisioning_uri(request.user.email, secret)
            return render(request, 'accounts/two_factor_setup.html', {
                'secret': secret,
                'uri': uri,
                'backup_codes': backup_codes,
                'step': 'confirm'
            })

        elif action == 'confirm':
            code = request.POST.get('code', '').strip()
            secret = request.session.get('setup_2fa_secret')
            backup_codes = request.session.get('setup_2fa_backup_codes', [])

            if secret and TOTPService.verify_totp(secret, code):
                two_factor.secret_key = secret
                two_factor.is_enabled = True
                two_factor.confirmed_at = timezone.now()
                # Hash backup codes for secure storage
                hashed_codes = [TOTPService.hash_backup_code(c) for c in backup_codes]
                two_factor.backup_codes = json.dumps(hashed_codes)
                two_factor.save()

                request.session.pop('setup_2fa_secret', None)
                request.session.pop('setup_2fa_backup_codes', None)

                SecurityAuditLog.objects.create(
                    user=request.user,
                    action='TWO_FACTOR_ENABLED',
                    module='accounts'
                )

                messages.success(request, 'Two-Factor Authentication is now active! Your account is protected.')
                return redirect('accounts:two_factor_setup')
            else:
                messages.error(request, 'Verification code was incorrect. Please try again.')
                uri = TOTPService.get_provisioning_uri(request.user.email, secret)
                return render(request, 'accounts/two_factor_setup.html', {
                    'secret': secret,
                    'uri': uri,
                    'backup_codes': backup_codes,
                    'step': 'confirm'
                })

        elif action == 'disable':
            password = request.POST.get('password', '')
            if request.user.check_password(password):
                two_factor.is_enabled = False
                two_factor.secret_key = ''
                two_factor.backup_codes = '[]'
                two_factor.save()

                SecurityAuditLog.objects.create(
                    user=request.user,
                    action='TWO_FACTOR_DISABLED',
                    module='accounts'
                )
                messages.info(request, 'Two-Factor Authentication has been disabled.')
                return redirect('accounts:two_factor_setup')
            else:
                messages.error(request, 'Incorrect account password.')

    return render(request, 'accounts/two_factor_setup.html', {
        'two_factor': two_factor,
        'step': 'status' if two_factor.is_enabled else 'intro'
    })


def password_reset_request_view(request):
    """Initiates self-service password reset request."""
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        success, raw_token, msg = PasswordResetService.request_reset(
            email=email,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        # In local/demo mode, we also provide the direct link if generated
        reset_link = None
        if raw_token:
            reset_link = request.build_absolute_uri(f'/accounts/password_reset/{raw_token}/')

        return render(request, 'accounts/password_reset_sent.html', {
            'email': email,
            'demo_reset_link': reset_link
        })

    return render(request, 'accounts/password_reset_request.html')


def password_reset_confirm_view(request, token):
    """Validates reset token and sets new password."""
    token_obj, err = PasswordResetService.validate_token(token)
    if err:
        messages.error(request, err)
        return redirect('accounts:password_reset_request')

    if request.method == 'POST':
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        success, msg = PasswordResetService.execute_password_reset(
            raw_token=token,
            new_password=new_password,
            confirm_password=confirm_password,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        if success:
            messages.success(request, msg)
            return redirect('accounts:login')
        else:
            messages.error(request, msg)

    return render(request, 'accounts/password_reset_confirm.html', {'token': token})


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
    two_factor = getattr(request.user, 'two_factor', None)
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
        preference.language = request.POST.get('language', 'en-us')
        preference.save()

        messages.success(request, 'Profile and preferences updated.')

    return render(request, 'accounts/profile.html', {
        'addresses': addresses,
        'preference': preference,
        'saved_payments': saved_payments,
        'two_factor': two_factor,
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


@login_required
def payment_methods_view(request):
    """Manages customer saved cards with PCI-DSS tokenized vault simulation."""
    cards = request.user.saved_payment_methods.all().order_by('-is_default', '-created_at')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            card_number = request.POST.get('card_number', '').replace(' ', '').replace('-', '')
            expiry_month = request.POST.get('expiry_month')
            expiry_year = request.POST.get('expiry_year')
            is_default = request.POST.get('is_default') == 'on'

            # Basic card brand detection
            brand = 'Visa'
            if card_number.startswith('4'):
                brand = 'Visa'
            elif card_number.startswith(('51', '52', '53', '54', '55')):
                brand = 'Mastercard'
            elif card_number.startswith(('34', '37')):
                brand = 'American Express'
            elif card_number.startswith('6011'):
                brand = 'Discover'

            if len(card_number) < 13 or not card_number.isdigit():
                messages.error(request, 'Invalid card number length.')
                return redirect('accounts:payment_methods')

            last4 = card_number[-4:]
            try:
                m = int(expiry_month)
                y = int(expiry_year)
                AccountsService.add_saved_payment_method(
                    user=request.user,
                    card_brand=brand,
                    last4=last4,
                    expiry_month=m,
                    expiry_year=y,
                    is_default=is_default
                )
                messages.success(request, f'Saved {brand} ending in {last4} to payment vault.')
            except ValueError:
                messages.error(request, 'Invalid expiry month or year.')

            return redirect('accounts:payment_methods')

    return render(request, 'accounts/payment_methods.html', {'cards': cards})


@login_required
def delete_payment_method_view(request, payment_id):
    SavedPaymentMethod.objects.filter(id=payment_id, user=request.user).delete()
    messages.info(request, 'Payment method removed.')
    return redirect('accounts:payment_methods')


@login_required
def set_default_payment_method_view(request, payment_id):
    card = get_object_or_404(SavedPaymentMethod, id=payment_id, user=request.user)
    card.is_default = True
    card.save()
    messages.success(request, f'{card.card_brand} ending in {card.last4} set as primary payment method.')
    return redirect('accounts:payment_methods')


@login_required
def privacy_dashboard_view(request):
    """GDPR / CCPA user privacy control center."""
    deletion_requests = request.user.deletion_requests.all().order_by('-requested_at')
    return render(request, 'accounts/privacy.html', {
        'deletion_requests': deletion_requests
    })


@login_required
def export_user_data_view(request):
    """Downloads machine-readable JSON data archive under GDPR Article 20."""
    archive = PrivacyService.generate_full_data_archive(request.user)
    payload = json.dumps(archive, indent=2)
    response = HttpResponse(payload, content_type='application/json')
    filename = f"shopsphere_gdpr_export_{request.user.id}_{timezone.now().strftime('%Y%m%d')}.json"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def request_account_deletion_view(request):
    """Submits or executes an account erasure request."""
    if request.method == 'POST':
        password = request.POST.get('password', '')
        reason = request.POST.get('reason', 'Self-service GDPR Right to Erasure')

        if not request.user.check_password(password):
            messages.error(request, 'Incorrect account password verification.')
            return redirect('accounts:privacy')

        # Execute erasure
        PrivacyService.execute_right_to_be_forgotten(request.user, reason)
        logout(request)
        messages.info(request, 'Your personal data has been erased from ShopSphere in compliance with GDPR.')
        return redirect('catalog:home')

    return redirect('accounts:privacy')
