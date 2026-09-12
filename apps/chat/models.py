from django.db import models
import uuid
from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.orders.models import Order

def generate_chn_id(): return f"chn_{uuid.uuid4().hex[:12]}"
def generate_msg_id(): return f"msg_{uuid.uuid4().hex[:12]}"
def generate_bkr_id(): return f"bkr_{uuid.uuid4().hex[:12]}"

class ChatChannel(models.Model):
    CHANNEL_TYPES = [
        ('SUPPORT_TRIAGE', '24/7 Automated Support & Helpdesk'),
        ('SELLER_INQUIRY', 'Customer to Seller Direct Inquiry'),
        ('ORDER_DISPUTE', 'Order Fulfillment Dispute'),
    ]
    STATUS_CHOICES = [
        ('OPEN', 'Active Open Channel'),
        ('WAITING_ON_AGENT', 'Queued for Human Support Specialist'),
        ('WAITING_ON_CUSTOMER', 'Waiting for Customer Reply'),
        ('RESOLVED', 'Issue Resolved'),
        ('CLOSED', 'Channel Closed'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_chn_id)
    channel_code = models.CharField(max_length=50, unique=True, default=uuid.uuid4)
    channel_type = models.CharField(max_length=30, choices=CHANNEL_TYPES, default='SUPPORT_TRIAGE')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_channels')
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_inquiries')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_threads')
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_support_chats')
    subject = models.CharField(max_length=200, default='Order & General Marketplace Assistance')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat {self.channel_code[:8]} ({self.customer.username} - {self.status})"


class ChatMessage(models.Model):
    SENDER_ROLES = [
        ('CUSTOMER', 'Shopper / Buyer'),
        ('SELLER', 'Merchant Partner'),
        ('SUPPORT_AGENT', 'Human Support Specialist'),
        ('AI_BOT', 'ShopSphere Automated Virtual Assistant'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_msg_id)
    channel = models.ForeignKey(ChatChannel, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_chat_messages')
    sender_role = models.CharField(max_length=20, choices=SENDER_ROLES, default='CUSTOMER')
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.sender_role}] {self.body[:40]}"


class BotKnowledgeRule(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_bkr_id)
    intent_tag = models.CharField(max_length=50, unique=True)
    keyword_triggers = models.CharField(max_length=255, help_text="Comma-separated trigger keywords")
    automated_response = models.TextField()
    should_escalate_to_human = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Rule: {self.intent_tag} (Keywords: {self.keyword_triggers[:30]})"

    def matches(self, text):
        text_lower = text.lower()
        triggers = [t.strip().lower() for t in self.keyword_triggers.split(',') if t.strip()]
        return any(trigger in text_lower for trigger in triggers)
