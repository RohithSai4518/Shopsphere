from django.db import models
from decimal import Decimal
import uuid
from apps.orders.models import Order, OrderItem
from apps.accounts.models import User

def generate_car_id(): return f"car_{uuid.uuid4().hex[:12]}"
def generate_whb_id(): return f"whb_{uuid.uuid4().hex[:12]}"
def generate_fzn_id(): return f"fzn_{uuid.uuid4().hex[:12]}"
def generate_pcl_id(): return f"pcl_{uuid.uuid4().hex[:12]}"
def generate_tcp_id(): return f"tcp_{uuid.uuid4().hex[:12]}"
def generate_mnf_id(): return f"mnf_{uuid.uuid4().hex[:12]}"

class Carrier(models.Model):
    CARRIER_TYPES = [
        ('EXPRESS', 'Express Air'),
        ('GROUND', 'Standard Ground'),
        ('FREIGHT', 'Heavy Freight'),
        ('LOCAL', 'Same-Day Courier'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_car_id)
    carrier_code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100)
    carrier_type = models.CharField(max_length=20, choices=CARRIER_TYPES, default='GROUND')
    tracking_url_template = models.CharField(max_length=255, default='https://track.shopsphere.internal/?id={tracking_number}')
    base_rate_per_kg = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('2.50'))
    minimum_fee = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('4.99'))
    standard_sla_days = models.PositiveIntegerField(default=3)
    supports_prime_expedited = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.carrier_code})"


class WarehouseHub(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_whb_id)
    hub_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=10, default='US')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('37.774900'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('-122.419400'))
    capacity_sqft = models.PositiveIntegerField(default=100000)
    current_utilization_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('65.00'))
    contact_phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hub_code} - {self.name} ({self.city}, {self.state})"


class FulfillmentZone(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_fzn_id)
    zone_code = models.CharField(max_length=30, unique=True)
    primary_hub = models.ForeignKey(WarehouseHub, on_delete=models.CASCADE, related_name='fulfillment_zones')
    postal_prefix = models.CharField(max_length=10, db_index=True)
    state_code = models.CharField(max_length=10)
    sla_transit_hours = models.PositiveIntegerField(default=48)
    express_eligible = models.BooleanField(default=True)

    def __str__(self):
        return f"Zone {self.zone_code} ({self.state_code}-{self.postal_prefix} -> {self.primary_hub.hub_code})"


class ShipmentParcel(models.Model):
    PARCEL_STATUS_CHOICES = [
        ('LABEL_CREATED', 'Shipping Label Generated'),
        ('PACKED', 'Packed in Facility'),
        ('DISPATCHED', 'Dispatched from Hub'),
        ('IN_TRANSIT', 'In Transit Between Hubs'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered to Recipient'),
        ('EXCEPTION', 'Delivery Exception / Delayed'),
        ('RETURNED_TO_ORIGIN', 'Returned to Origin (RTO)'),
    ]
    id = models.CharField(max_length=64, primary_key=True, default=generate_pcl_id)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='logistics_parcels')
    hub = models.ForeignKey(WarehouseHub, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatched_parcels')
    carrier = models.ForeignKey(Carrier, on_delete=models.PROTECT, related_name='parcels')
    tracking_number = models.CharField(max_length=100, unique=True, db_index=True)
    packing_slip_number = models.CharField(max_length=50, unique=True)
    length_cm = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('30.00'))
    width_cm = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('20.00'))
    height_cm = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('15.00'))
    actual_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('1.20'))
    volumetric_weight_kg = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('1.80'))
    shipping_fee_charged = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=30, choices=PARCEL_STATUS_CHOICES, default='LABEL_CREATED')
    current_location_desc = models.CharField(max_length=150, default='Origin Fulfillment Center')
    recipient_name = models.CharField(max_length=100)
    recipient_address_line = models.CharField(max_length=255)
    recipient_city = models.CharField(max_length=100)
    recipient_state = models.CharField(max_length=50)
    recipient_postal_code = models.CharField(max_length=20)
    estimated_delivery = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parcel {self.tracking_number} [{self.status}]"

    def compute_volumetric_weight(self):
        # Dimensional factor standard 5000 cm3/kg
        volume = self.length_cm * self.width_cm * self.height_cm
        return round(Decimal(volume) / Decimal('5000.00'), 2)


class TrackingCheckpoint(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_tcp_id)
    parcel = models.ForeignKey(ShipmentParcel, on_delete=models.CASCADE, related_name='checkpoints')
    milestone_name = models.CharField(max_length=100)
    facility_name = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=10, default='US')
    status_code = models.CharField(max_length=30)
    checkpoint_notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.parcel.tracking_number} - {self.milestone_name} @ {self.city}, {self.state}"


class DispatchManifest(models.Model):
    id = models.CharField(max_length=64, primary_key=True, default=generate_mnf_id)
    manifest_number = models.CharField(max_length=50, unique=True)
    hub = models.ForeignKey(WarehouseHub, on_delete=models.CASCADE, related_name='manifests')
    carrier = models.ForeignKey(Carrier, on_delete=models.PROTECT, related_name='manifests')
    driver_name = models.CharField(max_length=100, blank=True)
    vehicle_registration = models.CharField(max_length=50, blank=True)
    total_packages = models.PositiveIntegerField(default=0)
    total_weight_kg = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    dispatched_at = models.DateTimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Manifest {self.manifest_number} ({self.carrier.carrier_code} - {self.total_packages} pkgs)"
