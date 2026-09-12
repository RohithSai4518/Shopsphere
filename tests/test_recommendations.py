from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant
from apps.recommendations.models import ProductSimilarity, FrequentlyBoughtTogether, UserCategoryAffinity
from apps.recommendations.services import RecommendationEngine

class RecommendationsSubsystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='recs_user@example.com',
            email='recs_user@example.com',
            password='Password123!'
        )
        self.seller = Seller.objects.create(
            user=self.user,
            business_name='Tech MegaStore',
            business_email='tech@example.com',
            status='APPROVED'
        )
        self.cat_laptops = Category.objects.create(name='Laptops', slug='laptops-recs')
        self.cat_accessories = Category.objects.create(name='Accessories', slug='accessories-recs')

        self.laptop = Product.objects.create(
            name='Pro Ultra Laptop 16-inch',
            slug='pro-ultra-laptop',
            category=self.cat_laptops,
            seller=self.seller,
            base_price=Decimal('1200.00'),
            status='PUBLISHED'
        )
        self.v_laptop = ProductVariant.objects.create(
            product=self.laptop,
            sku='LAP-01',
            variant_name='16GB RAM',
            price_override=Decimal('1200.00')
        )

        self.mouse = Product.objects.create(
            name='Wireless Ergonomic Mouse',
            slug='wireless-ergo-mouse',
            category=self.cat_accessories,
            seller=self.seller,
            base_price=Decimal('50.00'),
            status='PUBLISHED'
        )
        self.v_mouse = ProductVariant.objects.create(
            product=self.mouse,
            sku='MSE-01',
            variant_name='Ergonomic Black',
            price_override=Decimal('50.00')
        )

        self.sleeve = Product.objects.create(
            name='Waterproof Laptop Sleeve',
            slug='waterproof-sleeve',
            category=self.cat_accessories,
            seller=self.seller,
            base_price=Decimal('30.00'),
            status='PUBLISHED'
        )
        self.v_sleeve = ProductVariant.objects.create(
            product=self.sleeve,
            sku='SLV-01',
            variant_name='Grey Sleeve',
            price_override=Decimal('30.00')
        )

    def test_frequently_bought_together_pricing(self):
        fbt = FrequentlyBoughtTogether.objects.create(
            base_product=self.laptop,
            bundle_item_1=self.mouse,
            bundle_item_2=self.sleeve,
            bundle_discount_pct=Decimal('10.00')
        )
        pricing = fbt.compute_bundle_pricing()
        # Original: 1200 + 50 + 30 = 1280
        # 10% discount: 1280 * 0.9 = 1152.00
        # Savings: 128.00
        self.assertEqual(pricing['original_price'], Decimal('1280.00'))
        self.assertEqual(pricing['bundled_price'], Decimal('1152.00'))
        self.assertEqual(pricing['savings'], Decimal('128.00'))

    def test_dynamic_bundle_generation(self):
        # Without pre-created FBT, verify dynamic fallback
        bundle_data = RecommendationEngine.get_frequently_bought_bundle(self.mouse)
        self.assertIsNotNone(bundle_data)
        self.assertIn(self.mouse, bundle_data['items'])

    def test_user_category_affinity_tracking(self):
        # Record view
        RecommendationEngine.record_user_view(self.user, self.laptop)
        aff = UserCategoryAffinity.objects.get(user=self.user, category=self.cat_laptops)
        self.assertEqual(aff.view_count, 1)

        # Record second view
        RecommendationEngine.record_user_view(self.user, self.laptop)
        aff.refresh_from_db()
        self.assertEqual(aff.view_count, 2)

    def test_personalized_feed(self):
        # When affinity is recorded for laptops, feed includes laptop
        RecommendationEngine.record_user_view(self.user, self.laptop)
        feed = RecommendationEngine.get_personalized_feed(self.user, limit=5)
        self.assertIn(self.laptop, feed)

    def test_recommendation_views_and_api(self):
        self.client.force_login(self.user)
        resp_feed = self.client.get(reverse('recommendations:for_you'))
        self.assertEqual(resp_feed.status_code, 200)
        self.assertContains(resp_feed, 'Recommended For You')

        resp_bundle = self.client.get(reverse('recommendations:bundle_explorer', args=[self.laptop.id]))
        self.assertEqual(resp_bundle.status_code, 200)
        self.assertContains(resp_bundle, 'Frequently Bought Together')

        resp_api = self.client.get(reverse('recommendations:api_similar', args=[self.laptop.id]))
        self.assertEqual(resp_api.status_code, 200)
        self.assertEqual(resp_api.json()['status'], 'success')
