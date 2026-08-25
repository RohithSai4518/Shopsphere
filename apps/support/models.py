from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from apps.accounts.models import User
from apps.orders.models import Order

def generate_tkt_id(): return f"tkt_{uuid.uuid4().hex[:12]}"
def generate_msg_id(): return f"msg_{uuid.uuid4().hex[:12]}"
def generate_cst_id(): return f"cst_{uuid.uuid4().hex[:12]}"

class SupportTicket(models.Model):
    CATEGORY_CHOICES = [
        ('GENERAL', 'General Query'),
        ('ORDER_ISSUE', 'Order Issue / Shipping'),
        ('REFUND', 'Refund / RMA Request'),
        ('TECHNICAL', 'Technical Platform Support'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low Priority'),
        ('MEDIUM', 'Medium SLA Priority'),
        ('HIGH', 'High Priority'),
        ('URGENT', 'Urgent Escalation'),
    ]
    STATUS_CHOICES = [
        ('OPEN', 'Open Ticket'),
        ('IN_PROGRESS', 'Agent Responded / In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_tkt_id)
    ticket_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_support_tickets')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='support_tickets')
    subject = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='GENERAL')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='OPEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.ticket_number} - {self.subject} ({self.status})"


class SupportMessage(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_msg_id)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_support_messages')
    message = models.TextField()
    is_internal_note = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message on {self.ticket.ticket_number} by {self.sender.first_name}"


class SupportSatisfactionRating(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_cst_id)
    ticket = models.OneToOneField(SupportTicket, on_delete=models.CASCADE, related_name='csat_rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='csat_ratings')
    rating_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    feedback_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
