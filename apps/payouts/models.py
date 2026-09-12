from django.db import models
from decimal import Decimal
import uuid
from apps.sellers.models import Seller
from apps.orders.models import Order, OrderItem
from apps.catalog.models import Category

def generate_esc_id(): return f"esc_{uuid.uuid4().hex[:12]}"
def generate_etx_id(): return f"etx_{uuid.uuid4().hex[:12]}"
def generate_bnk_id(): return f"bnk_{uuid.uuid4().hex[:12]}"
def generate_pyb_id(): return f"pyb_{uuid.uuid4().hex[:12]}"
def generate_pyi_id(): return f"pyi_{uuid.uuid4().hex[:12]}"
def generate_cmr_id(): return f"cmr_{uuid.uuid4().hex[:12]}"

class SellerEscrowAccount(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_esc_id)
    seller = models.OneToOneField(Seller, on_delete=models.CASCADE, related_name='escrow_account')
    pending_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    available_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    withheld_disputed_balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    lifetime_earnings = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    lifetime_payouts = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    is_payout_hold = models.BooleanField(default=False)
    hold_reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Escrow - {self.seller.business_name} (Avail: ${self.available_balance} / Pend: ${self.pending_balance})"


class EscrowTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('ORDER_HOLD', 'Order Payment Held in Escrow'),
        ('RETURN_WINDOW_RELEASE', 'Released to Available Balance'),
        ('RETURN_CLAWBACK', 'Refund Deduction for Customer Return'),
        ('DISPUTE_HOLD', 'Hold for Chargeback / Dispute'),
        ('COMMISSION_DEDUCTION', 'Marketplace Referral Fee Deduction'),
        ('PAYOUT_SETTLEMENT', 'Transfer Out via Payout Batch'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_etx_id)
    account = models.ForeignKey(SellerEscrowAccount, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='escrow_transactions')
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPES)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2)
    release_eligible_at = models.DateTimeField(null=True, blank=True)
    is_released = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type} (${self.net_amount}) - {self.account.seller.business_name}"


class SellerBankAccount(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_bnk_id)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='bank_accounts')
    bank_name = models.CharField(max_length=100)
    account_holder_name = models.CharField(max_length=150)
    routing_number = models.CharField(max_length=50)
    account_number_last4 = models.CharField(max_length=4)
    account_type = models.CharField(max_length=20, default='CHECKING')
    is_primary = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank_name} (*{self.account_number_last4}) - {self.account_holder_name}"


class PayoutBatch(models.Model):
    BATCH_STATUS = [
        ('DRAFT', 'Draft Calculation'),
        ('APPROVED', 'Approved for Settlement'),
        ('PROCESSING', 'Processing with Clearinghouse'),
        ('COMPLETED', 'Disbursed to Sellers'),
        ('FAILED', 'Disbursement Failed'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_pyb_id)
    batch_reference = models.CharField(max_length=50, unique=True)
    cycle_start = models.DateField()
    cycle_end = models.DateField()
    total_sellers_count = models.PositiveIntegerField(default=0)
    total_gross_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_commission_retained = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_net_disbursed = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=BATCH_STATUS, default='DRAFT')
    executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Batch {self.batch_reference} (${self.total_net_disbursed} - {self.status})"


class PayoutItem(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_pyi_id)
    batch = models.ForeignKey(PayoutBatch, on_delete=models.CASCADE, related_name='items')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='payout_items')
    bank_account = models.ForeignKey(SellerBankAccount, on_delete=models.SET_NULL, null=True, blank=True)
    gross_sales = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)
    refund_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_payout = models.DecimalField(max_digits=10, decimal_places=2)
    is_settled = models.BooleanField(default=False)
    transfer_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.seller.business_name}: Net ${self.net_payout} in {self.batch.batch_reference}"


class SellerCommissionRule(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_cmr_id)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='commission_rules', null=True, blank=True)
    tier_name = models.CharField(max_length=50, default='Standard Category Fee')
    fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00')) # e.g. 10%
    minimum_fee = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.50'))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        cat_name = self.category.name if self.category else 'Default General Rate'
        return f"{cat_name}: {self.fee_percentage}% (Min: ${self.minimum_fee})"
