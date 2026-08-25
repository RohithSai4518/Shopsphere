from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
from apps.accounts.models import User
from apps.catalog.models import Product

def generate_rev_id(): return f"rev_{uuid.uuid4().hex[:12]}"
def generate_rep_id(): return f"rep_{uuid.uuid4().hex[:12]}"

class Review(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Moderation'),
        ('APPROVED', 'Approved Review'),
        ('REJECTED', 'Rejected Review'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_rev_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=150, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    is_verified_purchase = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='APPROVED')
    helpful_votes = models.IntegerField(default=0)
    unhelpful_votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.product.name} - {self.rating} Stars by {self.user.first_name}"


class ReviewVote(models.Model):
    VOTE_TYPE_CHOICES = [
        ('HELPFUL', 'Helpful'),
        ('UNHELPFUL', 'Not Helpful'),
    ]
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_votes')
    vote_type = models.CharField(max_length=20, choices=VOTE_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')


class ReviewReport(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_rep_id)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_review_reports')
    reason = models.CharField(max_length=100)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
