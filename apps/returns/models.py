from django.db import models
from decimal import Decimal
import uuid
from apps.accounts.models import User
from apps.orders.models import Order, OrderItem

def generate_ret_id(): return f"ret_{uuid.uuid4().hex[:12]}"

class ReturnRequest(models.Model):
    STATUS_CHOICES = [
        ('SUBMITTED', 'Return Request Submitted'),
        ('APPROVED', 'Return Approved'),
        ('REJECTED', 'Return Rejected'),
        ('REFUNDED', 'Refund Processed'),
    ]
    REASON_CHOICES = [
        ('DEFECTIVE', 'Item Defective or Malfunctioning'),
        ('WRONG_ITEM', 'Wrong Item Delivered'),
        ('DAMAGED_IN_SHIPPING', 'Damaged During Transit'),
        ('CHANGED_MIND', 'Buyer Changed Mind'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_ret_id)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='returns')
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='returns')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='return_requests')
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, default='DEFECTIVE')
    comments = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUBMITTED')
    restocking_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    return_shipping_label_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RMA {self.id} - {self.get_reason_display()} ({self.status})"
