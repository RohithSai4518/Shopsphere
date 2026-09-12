from django.db import models
from decimal import Decimal
import uuid
from apps.accounts.models import User
from apps.orders.models import Order
from apps.catalog.models import ProductVariant

def generate_mtr_id(): return f"mtr_{uuid.uuid4().hex[:12]}"
def generate_ums_id(): return f"ums_{uuid.uuid4().hex[:12]}"
def generate_wal_id(): return f"wal_{uuid.uuid4().hex[:12]}"
def generate_rtx_id(): return f"rtx_{uuid.uuid4().hex[:12]}"
def generate_sub_id(): return f"sub_{uuid.uuid4().hex[:12]}"
def generate_sxl_id(): return f"sxl_{uuid.uuid4().hex[:12]}"

class MembershipTier(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_mtr_id)
    tier_code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200, default='Fast, free delivery and exclusive member benefits')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('14.99'))
    billing_period_days = models.PositiveIntegerField(default=30)
    free_shipping_min_spend = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    cashback_reward_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00')) # 5% back
    has_early_deal_access = models.BooleanField(default=True)
    has_free_same_day = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (${self.price}/{self.billing_period_days}d)"


class UserMembership(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active Member'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled by User'),
        ('PAYMENT_FAILED', 'Payment Renewal Failed'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_ums_id)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    tier = models.ForeignKey(MembershipTier, on_delete=models.PROTECT, related_name='active_members')
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    auto_renew = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.tier.name} ({self.status})"

    @property
    def is_valid(self):
        from django.utils import timezone
        return self.status == 'ACTIVE' and self.end_date > timezone.now()


class RewardWallet(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_wal_id)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reward_wallet')
    points_balance = models.PositiveIntegerField(default=0)
    lifetime_points_earned = models.PositiveIntegerField(default=0)
    lifetime_points_redeemed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet ({self.user.username}): {self.points_balance} pts (${self.cash_value:.2f})"

    @property
    def cash_value(self):
        # 100 points = $1.00 USD
        return Decimal(self.points_balance) / Decimal('100.00')


class RewardTransaction(models.Model):
    TX_TYPE_CHOICES = [
        ('PURCHASE_EARN', 'Points Earned on Purchase'),
        ('PRIME_BONUS', 'Prime Member Bonus Multiplier'),
        ('CHECKOUT_REDEEM', 'Points Redeemed at Checkout'),
        ('PROMO_GIFT', 'Special Promotional Credit'),
        ('REFUND_REVERSAL', 'Points Clawed Back for Return'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_rtx_id)
    wallet = models.ForeignKey(RewardWallet, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='reward_transactions')
    transaction_type = models.CharField(max_length=30, choices=TX_TYPE_CHOICES)
    points = models.IntegerField() # Positive for credit, negative for debit
    cash_equivalent = models.DecimalField(max_digits=8, decimal_places=2)
    balance_after = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type}: {self.points:+d} pts ({self.wallet.user.username})"


class SubscriptionPlan(models.Model):
    FREQUENCY_CHOICES = [
        (1, 'Every 1 Month (5% Discount)'),
        (2, 'Every 2 Months (10% Discount)'),
        (3, 'Every 3 Months (10% Discount)'),
        (6, 'Every 6 Months (15% Discount)'),
    ]
    STATUS_CHOICES = [
        ('ACTIVE', 'Active Auto-Delivery'),
        ('PAUSED', 'Paused by Customer'),
        ('CANCELLED', 'Cancelled'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_sub_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auto_subscriptions')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='active_subscriptions')
    quantity = models.PositiveIntegerField(default=1)
    frequency_months = models.PositiveIntegerField(choices=FREQUENCY_CHOICES, default=1)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('5.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    next_delivery_date = models.DateField()
    shipping_address_json = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Sub: {self.variant.sku} (x{self.quantity}) - {self.get_frequency_months_display()}"


class SubscriptionExecutionLog(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_sxl_id)
    subscription = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='execution_logs')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='SUCCESS')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Log {self.subscription.id} on {self.executed_at} [{self.status}]"
