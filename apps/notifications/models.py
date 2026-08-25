from django.db import models
import uuid
from apps.accounts.models import User

def generate_ntf_id(): return f"ntf_{uuid.uuid4().hex[:12]}"

class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('ORDER', 'Order Updates'),
        ('SHIPMENT', 'Shipment Tracking'),
        ('RETURN', 'RMA Return Status'),
        ('SELLER', 'Seller Merchant Notification'),
        ('PROMOTION', 'Promotional Campaign'),
        ('PRICE_DROP', 'Price Drop Alert'),
        ('STOCK_ALERT', 'Back in Stock Alert'),
        ('SUPPORT', 'Support Ticket Reply'),
        ('SYSTEM', 'System Security Alert'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_ntf_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPE_CHOICES, default='ORDER')
    action_url = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.title}"
