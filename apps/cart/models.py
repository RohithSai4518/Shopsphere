from django.db import models
from decimal import Decimal
import uuid
from apps.accounts.models import User
from apps.catalog.models import ProductVariant

def generate_crt_id(): return f"crt_{uuid.uuid4().hex[:12]}"
def generate_scrt_id(): return f"scrt_{uuid.uuid4().hex[:12]}"
def generate_scitem_id(): return f"scitem_{uuid.uuid4().hex[:12]}"

class CartItem(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_crt_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='cart_entries')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'variant')

    @property
    def unit_price(self):
        if self.variant.price_override is not None:
            return Decimal(str(self.variant.price_override))
        return Decimal(str(self.variant.product.base_price))

    @property
    def effective_unit_price(self):
        unit = self.unit_price
        disc = Decimal(str(self.variant.product.discount_percent))
        discount_val = (unit * disc) / Decimal('100.00')
        return round(unit - discount_val, 2)

    @property
    def subtotal(self):
        return round(self.effective_unit_price * Decimal(str(self.quantity)), 2)

    def __str__(self):
        return f"{self.user.email} - {self.variant.sku} (x{self.quantity})"


class SavedCart(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_scrt_id)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_carts')
    name = models.CharField(max_length=100, default='Saved Cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.name}"


class SavedCartItem(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_scitem_id)
    saved_cart = models.ForeignKey(SavedCart, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='saved_cart_entries')
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('saved_cart', 'variant')
