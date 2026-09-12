import unittest
from unittest import TestCase
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, Brand, ProductBundle, BundleItem
from apps.catalog.services import CatalogService
from django.contrib.auth import get_user_model

User = get_user_model()

class CatalogServiceTestCase(TestCase):
    def setUp(self):
        self.seller_user = User.objects.create_user(email='seller_svc@example.com', username='seller_svc@example.com', password='Pass', role='SELLER')
        self.seller = Seller.objects.create(user=self.seller_user, business_name='Tech Store', business_email='seller_svc@example.com')
        self.cat = Category.objects.create(name='Laptops', slug='laptops')
        self.brand = Brand.objects.create(name='ApexTech')

        self.p1 = Product.objects.create(seller=self.seller, category=self.cat, brand=self.brand, name='Apex Pro 15', slug='apex-pro-15', base_price=1200.00)
        self.p2 = Product.objects.create(seller=self.seller, category=self.cat, brand=self.brand, name='Apex Air 13', slug='apex-air-13', base_price=800.00)

    def test_search_products_by_query(self):
        res = CatalogService.search_products(query='Air')
        self.assertEqual(res.count(), 1)
        self.assertEqual(res.first().name, 'Apex Air 13')

    def test_search_products_price_filter(self):
        res = CatalogService.search_products(min_price=1000.00)
        self.assertEqual(res.count(), 1)
        self.assertEqual(res.first().name, 'Apex Pro 15')

    def test_search_products_ignores_empty_price_filters(self):
        res = CatalogService.search_products(category_slug='laptops', min_price='', max_price='')
        self.assertEqual(res.count(), 2)

    def test_bundle_savings_calculation(self):
        bundle = ProductBundle.objects.create(name='Pro Tech Pack', discount_percentage=15.00)
        BundleItem.objects.create(bundle=bundle, product=self.p1)
        BundleItem.objects.create(bundle=bundle, product=self.p2)

        savings = CatalogService.get_bundle_savings(bundle)
        self.assertEqual(savings['original_total'], 2000.00)
        self.assertEqual(savings['savings'], 300.00)
        self.assertEqual(savings['bundle_price'], 1700.00)
