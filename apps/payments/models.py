from django.db import models
from decimal import Decimal
import uuid
from apps.orders.models import Order

def generate_pay_id(): return f"pay_{uuid.uuid4().hex[:12]}"
def generate_led_id(): return f"led_{uuid.uuid4().hex[:12]}"
def generate_int_id(): return f"int_{uuid.uuid4().hex[:12]}"

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Payment Pending'),
        ('AUTHORIZED', 'Payment Authorized'),
        ('CAPTURED', 'Payment Captured'),
        ('SUCCESS', 'Payment Approved'),
        ('FAILED', 'Payment Declined'),
        ('REFUNDED', 'Payment Refunded'),
        ('PARTIALLY_REFUNDED', 'Partially Refunded'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_pay_id)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50, default='CREDIT_CARD_SANDBOX')
    transaction_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUCCESS')
    gateway_response_json = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_reference} - ${self.amount} ({self.status})"


class PaymentLedger(models.Model):
    ENTRY_TYPE_CHOICES = [
        ('AUTHORIZATION', 'Payment Authorization'),
        ('CAPTURE', 'Payment Capture'),
        ('REFUND', 'Refund Processing'),
        ('COMMISSION_FEE', 'Platform Commission Fee'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_led_id)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='ledger_entries')
    entry_type = models.CharField(max_length=30, choices=ENTRY_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PaymentIntent(models.Model):
    INTENT_STATUS_CHOICES = [
        ('CREATED', 'Intent Created'),
        ('REQUIRES_PAYMENT_METHOD', 'Requires Payment Method'),
        ('PROCESSING', 'Processing'),
        ('SUCCEEDED', 'Succeeded'),
        ('CANCELLED', 'Cancelled'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_int_id)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payment_intents')
    intent_token = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=INTENT_STATUS_CHOICES, default='CREATED')
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
