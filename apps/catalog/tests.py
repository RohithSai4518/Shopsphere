from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.sellers.models import Seller
from apps.catalog.models import Category, Brand, Product, ProductVariant
from .tests_expanded import ExpandedCatalogTestSuite

User = get_user_model()

class CatalogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='seller@apex.com',
            username='seller@apex.com',
            password='SellerPassword123!',
            role='SELLER'
        )
        self.seller = Seller.objects.create(
            user=self.user,
            business_name='Apex Tech',
            business_email='seller@apex.com'
        )
        self.category = Category.objects.create(name='Electronics', slug='electronics')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='Apex Laptop 15',
            slug='apex-laptop-15',
            base_price=1000.00,
            discount_percent=10.00
        )

    def test_effective_price_calculation(self):
        self.assertEqual(self.product.effective_price, 900.00)

    def test_product_variant_creation(self):
        variant = ProductVariant.objects.create(
            product=self.product,
            sku='APX-15-BLK',
            variant_name='Black Edition',
            price_override=950.00
        )
        self.assertEqual(variant.price_override, 950.00)
        self.assertEqual(variant.product.name, 'Apex Laptop 15')

class FullExpandedCatalogTests(ExpandedCatalogTestSuite):
    pass
