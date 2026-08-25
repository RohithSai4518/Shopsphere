from django.db import models
from decimal import Decimal
import uuid
from apps.accounts.models import User

def generate_seller_id(): return f"sel_{uuid.uuid4().hex[:12]}"
def generate_settlement_id(): return f"stl_{uuid.uuid4().hex[:12]}"
def generate_onboarding_id(): return f"onb_{uuid.uuid4().hex[:12]}"

class Seller(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved Merchant'),
        ('SUSPENDED', 'Suspended'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_seller_id)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    business_email = models.EmailField()
    business_phone = models.CharField(max_length=50, blank=True, null=True)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('8.50'))
    rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal('4.85'))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='APPROVED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.business_name} ({self.status})"


class SellerSettlement(models.Model):
    SETTLEMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending Processing'),
        ('PROCESSED', 'Payout Settled'),
        ('ON_HOLD', 'On Hold'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_settlement_id)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='settlements')
    period_start = models.DateTimeField()
    period_end = models.DateTimeField()
    gross_sales = models.DecimalField(max_digits=12, decimal_places=2)
    commission_fee = models.DecimalField(max_digits=12, decimal_places=2)
    net_payout = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=30, choices=SETTLEMENT_STATUS_CHOICES, default='PENDING')
    payout_reference = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Settlement {self.seller.business_name} - ${self.net_payout} ({self.status})"


class SellerOnboarding(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_onboarding_id)
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE, related_name='onboarding')
    is_identity_verified = models.BooleanField(default=False)
    is_bank_verified = models.BooleanField(default=False)
    is_tax_verified = models.BooleanField(default=False)
    current_step = models.IntegerField(default=1)
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
