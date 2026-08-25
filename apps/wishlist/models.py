from django.db import models
from decimal import Decimal
import uuid
from apps.accounts.models import User
from apps.catalog.models import Product, ProductVariant

def generate_wsh_id(): return f"wsh_{uuid.uuid4().hex[:12]}"
def generate_witem_id(): return f"witem_{uuid.uuid4().hex[:12]}"
def generate_palr_id(): return f"palr_{uuid.uuid4().hex[:12]}"
def generate_balr_id(): return f"balr_{uuid.uuid4().hex[:12]}"

class Wishlist(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_wsh_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    name = models.CharField(max_length=100, default='My Wishlist')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.name}"


class WishlistItem(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_witem_id)
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='in_wishlists')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('wishlist', 'product')


class PriceAlert(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_palr_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='price_alerts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_alerts')
    target_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_triggered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Price Alert {self.user.email} - {self.product.name} @ ${self.target_price}"


class BackInStockAlert(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_balr_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stock_alerts')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_alerts')
    is_notified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'variant')
