from django.db import models
from decimal import Decimal
import uuid
from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.catalog.models import Category

def generate_cpn_id(): return f"cpn_{uuid.uuid4().hex[:12]}"
def generate_cmp_id(): return f"cmp_{uuid.uuid4().hex[:12]}"
def generate_usg_id(): return f"usg_{uuid.uuid4().hex[:12]}"
def generate_gft_id(): return f"gft_{uuid.uuid4().hex[:12]}"

class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ('PERCENTAGE', 'Percentage Discount (%)'),
        ('FIXED', 'Fixed Amount Discount ($)'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_cpn_id)
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.IntegerField(default=1000)
    per_user_limit = models.IntegerField(default=1)
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True, related_name='coupons')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='coupons')
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_discount(self, subtotal):
        subtotal_dec = Decimal(str(subtotal))
        val_dec = Decimal(str(self.discount_value))
        min_dec = Decimal(str(self.min_order_subtotal))

        if subtotal_dec < min_dec:
            return Decimal('0.00')

        if self.discount_type == 'PERCENTAGE':
            disc = round((subtotal_dec * val_dec) / Decimal('100.00'), 2)
        else:
            disc = round(min(subtotal_dec, val_dec), 2)

        if self.max_discount_amount and disc > self.max_discount_amount:
            disc = self.max_discount_amount

        return disc

    def __str__(self):
        return f"{self.code} ({self.discount_value} {self.discount_type})"


class CouponUsage(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_usg_id)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='redemptions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupon_redemptions')
    order_id = models.CharField(max_length=64, blank=True, null=True)
    discount_applied = models.DecimalField(max_digits=10, decimal_places=2)
    used_at = models.DateTimeField(auto_now_add=True)


class PromotionalCampaign(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_cmp_id)
    title = models.CharField(max_length=200)
    banner_url = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('15.00'))
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class GiftCard(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_gft_id)
    code = models.CharField(max_length=50, unique=True)
    initial_balance = models.DecimalField(max_digits=10, decimal_places=2)
    current_balance = models.DecimalField(max_digits=10, decimal_places=2)
    pin_hash = models.CharField(max_length=255, blank=True, null=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GiftCard {self.code} (${self.current_balance} remaining)"
