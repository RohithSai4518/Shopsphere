import math
import uuid
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from .models import Carrier, WarehouseHub, ShipmentParcel, TrackingCheckpoint, DispatchManifest

class RoutingService:
    """
    Intelligent fulfillment router: determines optimal warehouse dispatch location
    based on proximity coordinates and current hub utilization capacity.
    """

    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculates distance in kilometers between two geographic coordinates."""
        R = 6371.0 # Earth radius in km
        phi1 = math.radians(float(lat1))
        phi2 = math.radians(float(lat2))
        delta_phi = math.radians(float(lat2) - float(lat1))
        delta_lambda = math.radians(float(lon2) - float(lon1))

        a = math.sin(delta_phi / 2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    @classmethod
    def select_optimal_hub(cls, dest_lat, dest_lon):
        """Finds closest active fulfillment center with available capacity."""
        hubs = WarehouseHub.objects.filter(is_active=True)
        if not hubs.exists():
            return None

        best_hub = None
        min_cost_score = float('inf')

        for hub in hubs:
            dist = cls.haversine_distance(dest_lat, dest_lon, hub.latitude, hub.longitude)
            # Weighted formula: 70% distance + 30% load utilization
            load_factor = float(hub.current_utilization_pct)
            score = (dist * 0.70) + (load_factor * 1.5)
            if score < min_cost_score:
                min_cost_score = score
                best_hub = hub

        return best_hub


class ShippingRateCalculator:
    """
    Calculates carrier freight rates based on chargeable weight, distance tier, and service SLA.
    """

    @staticmethod
    def calculate_rate(carrier, weight_kg, length_cm, width_cm, height_cm, is_prime=False):
        if is_prime and carrier.supports_prime_expedited:
            return Decimal('0.00')

        volumetric = (Decimal(length_cm) * Decimal(width_cm) * Decimal(height_cm)) / Decimal('5000.00')
        chargeable_weight = max(Decimal(weight_kg), volumetric)

        rate = carrier.minimum_fee + (chargeable_weight * carrier.base_rate_per_kg)
        return round(rate, 2)


class TrackingService:
    """
    Manages parcel state transitions, checkpoint milestones, and delivery event emission.
    """

    @classmethod
    def record_checkpoint(cls, parcel, milestone_name, facility_name, city, state, status_code, notes=""):
        checkpoint = TrackingCheckpoint.objects.create(
            parcel=parcel,
            milestone_name=milestone_name,
            facility_name=facility_name,
            city=city,
            state=state,
            status_code=status_code,
            checkpoint_notes=notes
        )
        parcel.status = status_code
        parcel.current_location_desc = f"{facility_name}, {city}, {state}"
        if status_code == 'DELIVERED':
            parcel.delivered_at = timezone.now()
        parcel.save()
        return checkpoint

    @classmethod
    def create_parcel_for_order(cls, order, carrier, hub=None, weight_kg=1.5, length_cm=30, width_cm=20, height_cm=15):
        tracking_no = f"TRK{uuid.uuid4().hex[:10].upper()}"
        packing_slip_no = f"PS-{uuid.uuid4().hex[:8].upper()}"

        estimated_eta = timezone.now() + timedelta(days=carrier.standard_sla_days)

        shipping_address = {}
        if hasattr(order, 'shipping_address_json'):
            import json
            try:
                shipping_address = json.loads(order.shipping_address_json)
            except Exception:
                pass

        recipient_name = shipping_address.get('full_name', order.user.username)
        addr_line = shipping_address.get('street_address', '100 Main St')
        city = shipping_address.get('city', 'Seattle')
        state = shipping_address.get('state', 'WA')
        zip_code = shipping_address.get('postal_code', '98101')

        parcel = ShipmentParcel.objects.create(
            order=order,
            hub=hub,
            carrier=carrier,
            tracking_number=tracking_no,
            packing_slip_number=packing_slip_no,
            length_cm=Decimal(str(length_cm)),
            width_cm=Decimal(str(width_cm)),
            height_cm=Decimal(str(height_cm)),
            actual_weight_kg=Decimal(str(weight_kg)),
            volumetric_weight_kg=round((Decimal(length_cm)*Decimal(width_cm)*Decimal(height_cm))/Decimal(5000), 2),
            shipping_fee_charged=order.shipping_amount,
            status='LABEL_CREATED',
            recipient_name=recipient_name,
            recipient_address_line=addr_line,
            recipient_city=city,
            recipient_state=state,
            recipient_postal_code=zip_code,
            estimated_delivery=estimated_eta
        )

        # Record Initial Checkpoint
        cls.record_checkpoint(
            parcel=parcel,
            milestone_name="Shipping Label Generated",
            facility_name=hub.name if hub else "Origin Fulfillment Center",
            city=hub.city if hub else city,
            state=hub.state if hub else state,
            status_code="LABEL_CREATED",
            notes="Electronic shipping information received from marketplace."
        )

        return parcel
