from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

def generate_user_id(): return f"usr_{uuid.uuid4().hex[:12]}"
def generate_address_id(): return f"addr_{uuid.uuid4().hex[:12]}"
def generate_session_id(): return f"sess_{uuid.uuid4().hex[:12]}"
def generate_log_id(): return f"log_{uuid.uuid4().hex[:12]}"
def generate_reset_id(): return f"rst_{uuid.uuid4().hex[:12]}"
def generate_paymeth_id(): return f"spm_{uuid.uuid4().hex[:12]}"

class User(AbstractUser):
    ROLE_CHOICES = [
        ('CUSTOMER', 'Customer'),
        ('SELLER', 'Merchant Seller'),
        ('SUPPORT', 'Support Agent'),
        ('ADMIN', 'Platform Administrator'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_user_id)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='CUSTOMER')
    is_verified = models.BooleanField(default=True)
    status = models.CharField(max_length=30, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"


class Address(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('SHIPPING', 'Shipping Address'),
        ('BILLING', 'Billing Address'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_address_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPE_CHOICES, default='SHIPPING')
    full_name = models.CharField(max_length=150)
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=30)
    country = models.CharField(max_length=100, default='United States')
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.city}, {self.state}"


class UserSession(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_session_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='active_sessions')
    token_hash = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)


class LoginHistory(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_log_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, default='SUCCESS')
    created_at = models.DateTimeField(auto_now_add=True)


class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='preferences')
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    promotional_emails = models.BooleanField(default=True)
    theme = models.CharField(max_length=20, default='DARK')
    currency = models.CharField(max_length=10, default='USD')
    language = models.CharField(max_length=10, default='en-us')
    updated_at = models.DateTimeField(auto_now=True)


class PasswordResetToken(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_reset_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets')
    token_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class SavedPaymentMethod(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_paymeth_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_payment_methods')
    card_brand = models.CharField(max_length=50, default='Visa')
    last4 = models.CharField(max_length=4)
    expiry_month = models.IntegerField()
    expiry_year = models.IntegerField()
    gateway_token_ref = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            SavedPaymentMethod.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.card_brand} ending in {self.last4}"


class UserTwoFactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='two_factor')
    is_enabled = models.BooleanField(default=False)
    secret_key = models.CharField(max_length=64, blank=True)
    backup_codes = models.TextField(blank=True, default='[]', help_text="JSON list of SHA-256 hashed recovery codes")
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"2FA for {self.user.email} (Enabled: {self.is_enabled})"


class AccountDeletionRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('COMPLETED', 'Completed / Anonymized'),
        ('CANCELLED', 'Cancelled by User'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deletion_requests')
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    requested_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Deletion Request: {self.user.email} [{self.status}]"
