import unittest
from unittest import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant

User = get_user_model()

class StorefrontViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller_user = User.objects.create_user(email='seller_v@example.com', username='seller_v@example.com', password='Password123!', role='SELLER')
        self.seller = Seller.objects.create(user=self.seller_user, business_name='V Store', business_email='seller_v@example.com')
        self.category = Category.objects.create(name='Hardware', slug='hardware')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='Precision Router',
            slug='precision-router',
            base_price=150.00,
            status='PUBLISHED'
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('catalog:home'))
        self.assertEqual(response.status_code, 200)

    def test_product_list_view(self):
        response = self.client.get(reverse('catalog:product_list'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_view(self):
        response = self.client.get(reverse('catalog:product_detail', kwargs={'slug': 'precision-router'}))
        self.assertEqual(response.status_code, 200)
