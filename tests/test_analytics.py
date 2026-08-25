from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product
from apps.analytics.models import RecentlyViewed, SearchHistory
from apps.analytics.services import AnalyticsService

User = get_user_model()

class AnalyticsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='anl@example.com', username='anl@example.com', password='Password123!')
        self.seller_user = User.objects.create_user(email='sel_anl@example.com', username='sel_anl@example.com', password='Password123!', role='SELLER')
        self.seller = Seller.objects.create(user=self.seller_user, business_name='Anl Store', business_email='sel_anl@example.com')
        self.cat = Category.objects.create(name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(seller=self.seller, category=self.cat, name='Drone Pro', slug='drone-pro', base_price=500.00)

    def test_analytics_service_record_view(self):
        AnalyticsService.record_product_view(self.user, self.product)
        rv = RecentlyViewed.objects.filter(user=self.user, product=self.product).first()
        self.assertIsNotNone(rv)

    def test_analytics_service_record_search(self):
        AnalyticsService.record_search_query(self.user, 'drone', 5)
        sh = SearchHistory.objects.filter(user=self.user, query_text='drone').first()
        self.assertEqual(sh.result_count, 5)
