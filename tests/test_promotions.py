from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.promotions.models import Coupon, PromotionalCampaign

class PromotionsTestCase(TestCase):
    def setUp(self):
        now = timezone.now()
        self.coupon = Coupon.objects.create(
            code='DISCOUNT10',
            discount_type='PERCENTAGE',
            discount_value=10.00,
            min_order_subtotal=50.00,
            starts_at=now - timedelta(days=1),
            expires_at=now + timedelta(days=30)
        )

    def test_coupon_percentage_calculation(self):
        discount = self.coupon.calculate_discount(subtotal=200.00)
        self.assertEqual(discount, 20.00)

    def test_coupon_below_minimum_subtotal(self):
        discount = self.coupon.calculate_discount(subtotal=30.00)
        self.assertEqual(discount, 0.00)
