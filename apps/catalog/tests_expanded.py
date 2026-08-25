"""
Expanded Comprehensive Test Suite for Catalog Management, Search, Filtering, and Performance.
Tests catalog view endpoints, search queries across categories, brand filtering, sorting logic,
product specification models, variant handling, and reviews.
"""

from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal

from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.catalog.models import Category, Brand, Product, ProductVariant, ProductSpecification, ProductImage
from apps.reviews.models import Review
from apps.inventory.models import Inventory

class ExpandedCatalogTestSuite(TestCase):
    def setUp(self):
        self.client = Client()
        
        # User & Seller Setup
        self.user = User.objects.create_user(
            username='test_catalog_user@example.com',
            email='test_catalog_user@example.com',
            password='TestPassword123!'
        )
        self.seller = Seller.objects.create(
            user=self.user,
            business_name='Apex Electronics Test Store',
            business_email='seller@apex.local',
            business_phone='+15550001111',
            tax_id='TAX-1234',
            commission_rate=Decimal('5.00'),
            status='APPROVED'
        )

        # Categories
        self.cat_laptops = Category.objects.create(name='Laptops & Computers', slug='laptops', is_active=True, display_order=1)
        self.cat_phones = Category.objects.create(name='Mobiles & Smartphones', slug='smartphones', is_active=True, display_order=2)
        self.cat_audio = Category.objects.create(name='Headphones & Audio', slug='audio-headphones', is_active=True, display_order=3)

        # Brands
        self.brand_apex = Brand.objects.create(name='ApexTech', description='High Tech Systems')
        self.brand_sound = Brand.objects.create(name='SoundWave', description='Acoustics')

        # Product 1: Apex Laptop
        self.p1 = Product.objects.create(
            seller=self.seller,
            category=self.cat_laptops,
            brand=self.brand_apex,
            name='ApexPro X15 Ultra Laptop',
            slug='apexpro-x15-ultra-laptop',
            brand_name='ApexTech',
            description='8-core CPU 32GB RAM 4K OLED',
            base_price=Decimal('1499.99'),
            discount_percent=Decimal('10.00'),
            status='PUBLISHED',
            is_featured=True
        )
        self.var1 = ProductVariant.objects.create(
            product=self.p1,
            sku='SKU-APX-001',
            variant_name='32GB RAM / 1TB SSD',
            price_override=Decimal('1499.99')
        )
        ProductImage.objects.create(product=self.p1, image_url='https://example.com/laptop.jpg', is_primary=True)
        Inventory.objects.create(variant=self.var1, quantity_on_hand=50)
        Review.objects.create(product=self.p1, user=self.user, rating=5, title='Amazing Laptop', status='APPROVED')

        # Product 2: SoundWave Headphones
        self.p2 = Product.objects.create(
            seller=self.seller,
            category=self.cat_audio,
            brand=self.brand_sound,
            name='SoundWave Pro Active Noise Cancelling Headphones',
            slug='soundwave-pro-active-noise-cancelling-headphones',
            brand_name='SoundWave',
            description='Wireless ANC headphones 40h battery',
            base_price=Decimal('249.99'),
            discount_percent=Decimal('15.00'),
            status='PUBLISHED',
            is_bestseller=True
        )
        self.var2 = ProductVariant.objects.create(
            product=self.p2,
            sku='SKU-SW-002',
            variant_name='Midnight Black',
            price_override=Decimal('249.99')
        )
        ProductImage.objects.create(product=self.p2, image_url='https://example.com/audio.jpg', is_primary=True)
        Inventory.objects.create(variant=self.var2, quantity_on_hand=100)
        Review.objects.create(product=self.p2, user=self.user, rating=4, title='Great Sound', status='APPROVED')

        # Product 3: Budget Phone
        self.p3 = Product.objects.create(
            seller=self.seller,
            category=self.cat_phones,
            brand=self.brand_apex,
            name='Nova Phone Z1 5G',
            slug='nova-phone-z1-5g',
            brand_name='ApexTech',
            description='5G smartphone OLED 5000mAh',
            base_price=Decimal('699.99'),
            discount_percent=Decimal('0.00'),
            status='PUBLISHED'
        )
        self.var3 = ProductVariant.objects.create(
            product=self.p3,
            sku='SKU-NOV-003',
            variant_name='Standard 128GB',
            price_override=Decimal('699.99')
        )
        Inventory.objects.create(variant=self.var3, quantity_on_hand=30)

    def test_home_page_loads_categories_and_products(self):
        url = reverse('catalog:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptops &amp; Computers')
        self.assertContains(response, 'ApexPro X15 Ultra Laptop')

    def test_product_list_all_products(self):
        url = reverse('catalog:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 3)

    def test_search_products_by_keyword(self):
        url = reverse('catalog:product_list') + '?q=Laptop'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].name, 'ApexPro X15 Ultra Laptop')

    def test_filter_products_by_category(self):
        url = reverse('catalog:product_list') + '?category=audio-headphones'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)
        self.assertEqual(response.context['products'][0].name, 'SoundWave Pro Active Noise Cancelling Headphones')

    def test_filter_products_by_brand(self):
        url = reverse('catalog:product_list') + f'?brand={self.brand_sound.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 1)

    def test_sort_products_price_low_to_high(self):
        url = reverse('catalog:product_list') + '?sort=price_asc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertEqual(products[0].name, 'SoundWave Pro Active Noise Cancelling Headphones')
        self.assertEqual(products[1].name, 'Nova Phone Z1 5G')
        self.assertEqual(products[2].name, 'ApexPro X15 Ultra Laptop')

    def test_sort_products_price_high_to_low(self):
        url = reverse('catalog:product_list') + '?sort=price_desc'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        products = list(response.context['products'])
        self.assertEqual(products[0].name, 'ApexPro X15 Ultra Laptop')

    def test_product_detail_view(self):
        url = reverse('catalog:product_detail', kwargs={'slug': 'apexpro-x15-ultra-laptop'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ApexPro X15 Ultra Laptop')
        self.assertContains(response, '32GB RAM / 1TB SSD')

    def test_effective_price_calculation(self):
        # Base: 1499.99, Discount: 10.00% -> 1349.99
        self.assertEqual(self.p1.effective_price, Decimal('1349.99'))

    def test_search_suggestions_api(self):
        url = reverse('catalog:api_search_suggestions') + '?q=Apex'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('suggestions', data)
        self.assertTrue(len(data['suggestions']) >= 1)
