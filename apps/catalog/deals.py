from django.db import models
from django.utils import timezone
from decimal import Decimal
import uuid
from apps.accounts.models import User
from apps.catalog.models import Product

def generate_deal_id():
    return f"deal_{uuid.uuid4().hex[:12]}"

def generate_claim_id():
    return f"clm_{uuid.uuid4().hex[:12]}"

class LightningDeal(models.Model):
    STATUS_CHOICES = [
        ('UPCOMING', 'Upcoming'),
        ('ACTIVE', 'Active / Live'),
        ('ENDED', 'Ended'),
        ('SOLD_OUT', 'Sold Out'),
    ]

    id = models.CharField(max_length=64, primary_key=True, default=generate_deal_id)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lightning_deals')
    deal_title = models.CharField(max_length=200)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('20.00'))
    deal_price = models.DecimalField(max_digits=10, decimal_places=2)
    allocated_stock = models.PositiveIntegerField(default=50)
    claimed_units = models.PositiveIntegerField(default=0)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-starts_at']

    def __str__(self):
        return f"{self.deal_title} ({self.discount_percent}% off) - {self.product.name}"

    @property
    def is_live(self):
        now = timezone.now()
        return self.is_active and (self.starts_at <= now <= self.ends_at) and (self.claimed_units < self.allocated_stock)

    @property
    def is_sold_out(self):
        return self.claimed_units >= self.allocated_stock

    @property
    def percent_claimed(self):
        if self.allocated_stock <= 0:
            return 100
        return min(100, int((self.claimed_units / self.allocated_stock) * 100))

    @property
    def remaining_units(self):
        return max(0, self.allocated_stock - self.claimed_units)

    @property
    def time_remaining_seconds(self):
        now = timezone.now()
        if now >= self.ends_at:
            return 0
        return int((self.ends_at - now).total_seconds())

    @property
    def formatted_time_remaining(self):
        secs = self.time_remaining_seconds
        if secs <= 0:
            return "Ended"
        hours = secs // 3600
        mins = (secs % 3600) // 60
        remaining_secs = secs % 60
        return f"{hours:02d}h {mins:02d}m {remaining_secs:02d}s"


class LightningDealClaim(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_claim_id)
    deal = models.ForeignKey(LightningDeal, on_delete=models.CASCADE, related_name='claims')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deal_claims')
    claimed_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_purchased = models.BooleanField(default=False)

    class Meta:
        unique_together = ('deal', 'user')

    def __str__(self):
        return f"Claim by {self.user.email} on {self.deal.deal_title}"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at and not self.is_purchased


class DealService:
    @staticmethod
    def get_live_deals(category_slug=None, limit=20):
        try:
            now = timezone.now()
            qs = LightningDeal.objects.filter(
                is_active=True,
                starts_at__lte=now,
                ends_at__gte=now
            ).select_related('product', 'product__category', 'product__seller')

            if category_slug:
                qs = qs.filter(product__category__slug=category_slug)

            return list(qs.order_by('ends_at')[:limit])
        except Exception:
            return []

    @staticmethod
    def get_deal_for_product(product):
        try:
            now = timezone.now()
            return LightningDeal.objects.filter(
                product=product,
                is_active=True,
                starts_at__lte=now,
                ends_at__gte=now
            ).first()
        except Exception:
            return None

    @staticmethod
    def claim_deal(user, deal_id, reservation_minutes=15):
        from django.db import transaction
        with transaction.atomic():
            deal = LightningDeal.objects.select_for_update().get(id=deal_id)
            if not deal.is_live:
                return False, "Deal is not active or has expired."

            if deal.is_sold_out:
                return False, "Deal is 100% claimed."

            existing = LightningDealClaim.objects.filter(deal=deal, user=user).first()
            if existing:
                if not existing.is_expired:
                    return False, "You have already reserved this deal. Proceed to checkout."
                else:
                    existing.expires_at = timezone.now() + timezone.timedelta(minutes=reservation_minutes)
                    existing.save()
                    return True, "Deal claim reservation extended."

            expires = timezone.now() + timezone.timedelta(minutes=reservation_minutes)
            LightningDealClaim.objects.create(deal=deal, user=user, expires_at=expires)
            deal.claimed_units += 1
            deal.save()
            return True, "Deal claimed successfully!"
