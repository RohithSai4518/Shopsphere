from django.db import models
from decimal import Decimal
import uuid
from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.catalog.models import ProductVariant
from apps.promotions.models import Coupon

def generate_ord_id(): return f"ord_{uuid.uuid4().hex[:12]}"
def generate_ori_id(): return f"ori_{uuid.uuid4().hex[:12]}"
def generate_osh_id(): return f"osh_{uuid.uuid4().hex[:12]}"
def generate_shp_id(): return f"shp_{uuid.uuid4().hex[:12]}"
def generate_sev_id(): return f"sev_{uuid.uuid4().hex[:12]}"
def generate_exc_id(): return f"exc_{uuid.uuid4().hex[:12]}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Payment'),
        ('CONFIRMED', 'Order Confirmed'),
        ('PACKED', 'Packed in Warehouse'),
        ('PROCESSING', 'Processing Fulfillment'),
        ('SHIPPED', 'Shipped'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('RETURN_REQUESTED', 'Return Requested'),
        ('RETURNED', 'Returned'),
        ('REFUNDED', 'Refunded'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_ord_id)
    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    shipping_address_json = models.TextField(default='{}')
    billing_address_json = models.TextField(default='{}')
    estimated_delivery_date = models.DateField(null=True, blank=True)
    delivery_speed = models.CharField(max_length=30, default='STANDARD')
    is_gift = models.BooleanField(default=False)
    gift_message = models.TextField(blank=True)
    gift_wrap_type = models.CharField(max_length=30, default='NONE')
    gift_wrap_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    idempotency_key = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order_number} ({self.status}) - ${self.total_amount}"


class OrderItem(models.Model):
    ITEM_STATUS_CHOICES = [
        ('PENDING', 'Pending Fulfillment'),
        ('PACKED', 'Packed'),
        ('SHIPPED', 'Item Shipped'),
        ('DELIVERED', 'Item Delivered'),
        ('CANCELLED', 'Item Cancelled'),
        ('RETURNED', 'Item Returned'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_ori_id)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name='order_items')
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, related_name='fulfilled_items')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_status = models.CharField(max_length=30, choices=ITEM_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order.order_number} - {self.variant.sku} (x{self.quantity})"


class OrderStatusHistory(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_osh_id)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    from_status = models.CharField(max_length=30)
    to_status = models.CharField(max_length=30)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_status_changes')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Shipment(models.Model):
    SHIPMENT_STATUS_CHOICES = [
        ('LABEL_CREATED', 'Shipping Label Created'),
        ('IN_TRANSIT', 'In Transit'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Package Delivered'),
        ('FAILED_ATTEMPT', 'Delivery Attempt Failed'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_shp_id)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='shipments')
    carrier = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, unique=True)
    shipping_label_url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=30, choices=SHIPMENT_STATUS_CHOICES, default='LABEL_CREATED')
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.carrier} - {self.tracking_number} ({self.status})"


class ShipmentEvent(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_sev_id)
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name='events')
    location = models.CharField(max_length=150)
    status_description = models.CharField(max_length=255)
    event_timestamp = models.DateTimeField()

    class Meta:
        ordering = ['-event_timestamp']


class ExchangeRequest(models.Model):
    EXCHANGE_STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('COMPLETED', 'Exchange Completed'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_exc_id)
    order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='exchanges')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exchange_requests')
    target_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name='requested_exchanges')
    reason = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=EXCHANGE_STATUS_CHOICES, default='SUBMITTED')
    created_at = models.DateTimeField(auto_now_add=True)


def generate_inv_id(): return f"inv_{uuid.uuid4().hex[:12]}"

class OrderInvoice(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_inv_id)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)
    tax_identifier = models.CharField(max_length=50, default='US-EIN-94-3829101')
    subtotal_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.order.order_number}"
