from django.test import TestCase
from decimal import Decimal
from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.catalog.models import Category, Brand, Product, ProductVariant, ProductBundle, BundleItem
from apps.catalog.services import CatalogService

class CatalogServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='seller_cat@test.com', email='seller_cat@test.com', password='pass')
        self.seller = Seller.objects.create(user=self.user, business_name='Apex Electronics', business_email='seller_cat@test.com')
        self.category = Category.objects.create(name='Laptops', slug='laptops')
        self.brand = Brand.objects.create(name='ApexTech')

        self.p1 = Product.objects.create(
            seller=self.seller,
            category=self.category,
            brand=self.brand,
            name='Apex Book Pro 15',
            description='Flagship Workstation Laptop',
            base_price=Decimal('1500.00'),
            discount_percent=Decimal('10.00'),
            is_featured=True,
            status='PUBLISHED'
        )

        self.v1 = ProductVariant.objects.create(
            product=self.p1,
            sku='SKU-APX-15',
            variant_name='16GB RAM / 512GB SSD',
            price_override=Decimal('1500.00')
        )

    def test_search_products(self):
        results = CatalogService.search_products(query='Book')
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().name, 'Apex Book Pro 15')

    def test_effective_price_calculation(self):
        self.assertEqual(self.p1.effective_price, Decimal('1350.00'))

    def test_bundle_savings_calculation(self):
        bundle = ProductBundle.objects.create(name='Apex Creator Bundle', discount_percentage=Decimal('10.00'))
        BundleItem.objects.create(bundle=bundle, product=self.p1)

        summary = CatalogService.get_bundle_savings(bundle)
        self.assertEqual(summary['original_total'], Decimal('1350.00'))
        self.assertEqual(summary['bundle_price'], Decimal('1215.00'))
