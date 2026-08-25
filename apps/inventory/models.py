from django.db import models
from decimal import Decimal
import uuid
from apps.catalog.models import ProductVariant

def generate_wh_id(): return f"wh_{uuid.uuid4().hex[:12]}"
def generate_inv_id(): return f"inv_{uuid.uuid4().hex[:12]}"
def generate_itx_id(): return f"itx_{uuid.uuid4().hex[:12]}"
def generate_po_id(): return f"po_{uuid.uuid4().hex[:12]}"
def generate_poi_id(): return f"poi_{uuid.uuid4().hex[:12]}"

class WarehouseLocation(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_wh_id)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='United States')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Inventory(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_inv_id)
    variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE, related_name='inventory')
    quantity_on_hand = models.IntegerField(default=0)
    quantity_reserved = models.IntegerField(default=0)
    quantity_damaged = models.IntegerField(default=0)
    reorder_threshold = models.IntegerField(default=5)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def quantity_available(self):
        return max(0, self.quantity_on_hand - self.quantity_reserved - self.quantity_damaged)

    def __str__(self):
        return f"{self.variant.sku} - Available: {self.quantity_available} / Total: {self.quantity_on_hand}"


class InventoryTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('RECEIPT', 'Inventory Receipt / Restock'),
        ('DEDUCTION', 'Order Deduction'),
        ('RESERVATION', 'Checkout Reservation'),
        ('RELEASE', 'Reservation Release'),
        ('RETURN', 'RMA Return Credit'),
        ('DAMAGE_ADJUSTMENT', 'Damaged Stock Adjustment'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_itx_id)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=30, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField()
    reference_type = models.CharField(max_length=50, blank=True, null=True)
    reference_id = models.CharField(max_length=64, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PurchaseOrder(models.Model):
    PO_STATUS_CHOICES = [
        ('DRAFT', 'Draft PO'),
        ('SUBMITTED', 'Submitted to Supplier'),
        ('PARTIALLY_RECEIVED', 'Partially Received'),
        ('RECEIVED', 'Fully Received'),
        ('CANCELLED', 'Cancelled'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_po_id)
    po_number = models.CharField(max_length=50, unique=True)
    warehouse = models.ForeignKey(WarehouseLocation, on_delete=models.PROTECT, related_name='purchase_orders')
    supplier_name = models.CharField(max_length=200)
    status = models.CharField(max_length=30, choices=PO_STATUS_CHOICES, default='DRAFT')
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.po_number} - {self.supplier_name} ({self.status})"


class PurchaseOrderItem(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_poi_id)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name='po_items')
    quantity_ordered = models.IntegerField()
    quantity_received = models.IntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"PO {self.purchase_order.po_number} - {self.variant.sku} ({self.quantity_received}/{self.quantity_ordered})"
