from django.db import models
from decimal import Decimal
import uuid
from apps.accounts.models import User
from apps.catalog.models import Product

def generate_sch_id(): return f"sch_{uuid.uuid4().hex[:12]}"
def generate_prm_id(): return f"prm_{uuid.uuid4().hex[:12]}"
def generate_pdm_id(): return f"pdm_{uuid.uuid4().hex[:12]}"

class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recently_viewed_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='recent_views')
    viewed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product')


class SearchHistory(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_sch_id)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='search_history')
    query_text = models.CharField(max_length=255)
    result_count = models.IntegerField(default=0)
    searched_at = models.DateTimeField(auto_now_add=True)


class ProductAnalytics(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_prm_id)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='analytics')
    total_views = models.IntegerField(default=0)
    total_cart_additions = models.IntegerField(default=0)
    total_units_sold = models.IntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    updated_at = models.DateTimeField(auto_now=True)


class PlatformDailyMetric(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_pdm_id)
    metric_date = models.DateField(unique=True)
    gross_merchandise_value = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal('0.00'))
    order_count = models.IntegerField(default=0)
    active_customers = models.IntegerField(default=0)
    active_sellers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
