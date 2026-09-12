from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from apps.accounts.models import User
from apps.orders.models import Order
from apps.logistics.models import Carrier, WarehouseHub, ShipmentParcel, TrackingCheckpoint
from apps.logistics.services import RoutingService, ShippingRateCalculator, TrackingService

class LogisticsSubsystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='buyer_logistics@example.com',
            email='buyer_logistics@example.com',
            password='Password123!'
        )
        self.carrier_fedex = Carrier.objects.create(
            carrier_code='FEDEX_EXP',
            name='FedEx Express',
            carrier_type='EXPRESS',
            base_rate_per_kg=Decimal('3.00'),
            minimum_fee=Decimal('5.00'),
            standard_sla_days=2,
            supports_prime_expedited=True
        )
        self.carrier_ground = Carrier.objects.create(
            carrier_code='UPS_GRD',
            name='UPS Ground',
            carrier_type='GROUND',
            base_rate_per_kg=Decimal('1.50'),
            minimum_fee=Decimal('4.00'),
            standard_sla_days=4,
            supports_prime_expedited=False
        )
        self.hub_sea = WarehouseHub.objects.create(
            hub_code='SEA-01',
            name='Seattle Mega Fulfillment Center',
            street_address='100 Logistics Blvd',
            city='Seattle',
            state='WA',
            postal_code='98101',
            latitude=Decimal('47.6062'),
            longitude=Decimal('-122.3321'),
            capacity_sqft=250000,
            current_utilization_pct=Decimal('45.00')
        )
        self.hub_dal = WarehouseHub.objects.create(
            hub_code='DFW-02',
            name='Dallas Regional Hub',
            street_address='200 Cargo Rd',
            city='Dallas',
            state='TX',
            postal_code='75201',
            latitude=Decimal('32.7767'),
            longitude=Decimal('-96.7970'),
            capacity_sqft=180000,
            current_utilization_pct=Decimal('85.00')
        )
        self.order = Order.objects.create(
            order_number='ORD-LOG-9901',
            user=self.user,
            status='CONFIRMED',
            subtotal=Decimal('120.00'),
            tax_amount=Decimal('10.00'),
            shipping_amount=Decimal('5.99'),
            total_amount=Decimal('135.99'),
            shipping_address_json='{"full_name": "John Doe", "street_address": "500 Pine St", "city": "Seattle", "state": "WA", "postal_code": "98101"}'
        )

    def test_haversine_distance_and_optimal_hub_selection(self):
        # Customer in Portland, OR (close to Seattle)
        portland_lat = Decimal('45.5152')
        portland_lon = Decimal('-122.6784')
        best_hub = RoutingService.select_optimal_hub(portland_lat, portland_lon)
        self.assertIsNotNone(best_hub)
        self.assertEqual(best_hub.hub_code, 'SEA-01')

    def test_shipping_rate_calculation(self):
        # Weight 2kg, dimensions 20x20x20 => volumetric 1.6kg -> chargeable is 2kg
        rate = ShippingRateCalculator.calculate_rate(
            self.carrier_fedex, weight_kg=2.0, length_cm=20, width_cm=20, height_cm=20, is_prime=False
        )
        # min 5.00 + 2.0 * 3.00 = 11.00
        self.assertEqual(rate, Decimal('11.00'))

        # Prime shipping override
        prime_rate = ShippingRateCalculator.calculate_rate(
            self.carrier_fedex, weight_kg=5.0, length_cm=30, width_cm=30, height_cm=30, is_prime=True
        )
        self.assertEqual(prime_rate, Decimal('0.00'))

    def test_parcel_creation_and_checkpoints(self):
        parcel = TrackingService.create_parcel_for_order(
            order=self.order,
            carrier=self.carrier_fedex,
            hub=self.hub_sea,
            weight_kg=2.5
        )
        self.assertTrue(parcel.tracking_number.startswith('TRK'))
        self.assertEqual(parcel.status, 'LABEL_CREATED')
        self.assertEqual(parcel.checkpoints.count(), 1)

        # Record next transit milestone
        cp = TrackingService.record_checkpoint(
            parcel=parcel,
            milestone_name="Dispatched from Facility",
            facility_name="SEA-01 Fulfillment Hub",
            city="Seattle",
            state="WA",
            status_code="DISPATCHED",
            notes="Sorted into outbound freight flight."
        )
        self.assertEqual(parcel.status, 'DISPATCHED')
        self.assertEqual(parcel.checkpoints.count(), 2)

    def test_tracking_portal_and_api(self):
        parcel = TrackingService.create_parcel_for_order(
            order=self.order,
            carrier=self.carrier_fedex,
            hub=self.hub_sea
        )
        # View tracking portal
        url = reverse('logistics:track_detail', args=[parcel.tracking_number])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, parcel.tracking_number)

        # API tracking status
        api_url = reverse('logistics:api_tracking', args=[parcel.tracking_number])
        api_resp = self.client.get(api_url)
        self.assertEqual(api_resp.status_code, 200)
        data = api_resp.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['tracking_number'], parcel.tracking_number)
