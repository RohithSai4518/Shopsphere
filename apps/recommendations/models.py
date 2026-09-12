from django.db import models
from decimal import Decimal
import uuid
from apps.catalog.models import Product, Category
from apps.accounts.models import User

def generate_sim_id(): return f"sim_{uuid.uuid4().hex[:12]}"
def generate_fbt_id(): return f"fbt_{uuid.uuid4().hex[:12]}"
def generate_aff_id(): return f"aff_{uuid.uuid4().hex[:12]}"

class ProductSimilarity(models.Model):
    MATCH_TYPES = [
        ('CONTENT_SPECS', 'Attribute & Specifications Match'),
        ('CO_PURCHASE', 'Marketplace Co-Purchase Frequency'),
        ('CATEGORY_HYBRID', 'Hierarchical Category Nearest Neighbor'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_sim_id)
    source_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='similarities_from')
    target_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='similarities_to')
    similarity_score = models.DecimalField(max_digits=5, decimal_places=4, default=Decimal('0.8500')) # 0.0000 - 1.0000
    match_type = models.CharField(max_length=30, choices=MATCH_TYPES, default='CONTENT_SPECS')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('source_product', 'target_product', 'match_type')
        ordering = ['-similarity_score']

    def __str__(self):
        return f"{self.source_product.name[:20]} -> {self.target_product.name[:20]} ({self.similarity_score})"


class FrequentlyBoughtTogether(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_fbt_id)
    base_product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='frequently_bought_bundle')
    bundle_item_1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fbt_bundle_1')
    bundle_item_2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fbt_bundle_2', null=True, blank=True)
    bundle_discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('8.00')) # 8% combo discount
    co_occurrence_count = models.PositiveIntegerField(default=42)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bundle for {self.base_product.name} (Save {self.bundle_discount_pct}%)"

    def compute_bundle_pricing(self):
        v0 = self.base_product.variants.first()
        p0 = v0.price if v0 else Decimal('0.00')

        v1 = self.bundle_item_1.variants.first()
        p1 = v1.price if v1 else Decimal('0.00')

        p2 = Decimal('0.00')
        if self.bundle_item_2:
            v2 = self.bundle_item_2.variants.first()
            if v2: p2 = v2.price

        original_total = p0 + p1 + p2
        discount_factor = (Decimal('100.00') - self.bundle_discount_pct) / Decimal('100.00')
        bundled_total = round(original_total * discount_factor, 2)
        savings = original_total - bundled_total

        return {
            'original_price': original_total,
            'bundled_price': bundled_total,
            'savings': savings,
            'discount_pct': self.bundle_discount_pct
        }


class UserCategoryAffinity(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_aff_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='category_affinities')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='user_affinities')
    view_count = models.PositiveIntegerField(default=1)
    purchase_count = models.PositiveIntegerField(default=0)
    affinity_score = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('1.00'))
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'category')
        ordering = ['-affinity_score']

    def __str__(self):
        return f"{self.user.username} -> {self.category.name} ({self.affinity_score})"
