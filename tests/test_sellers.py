import unittest
from unittest import TestCase
from django.contrib.auth import get_user_model
from apps.sellers.models import Seller

User = get_user_model()

class SellerModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='merchant_test@example.com',
            username='merchant_test@example.com',
            password='Password123!',
            role='SELLER'
        )

    def test_seller_profile_creation(self):
        seller = Seller.objects.create(
            user=self.user,
            business_name='Apex Merchant Store',
            business_email='merchant_test@example.com',
            commission_rate=8.50
        )
        self.assertEqual(seller.business_name, 'Apex Merchant Store')
        self.assertEqual(seller.status, 'APPROVED')
        self.assertEqual(seller.user.role, 'SELLER')
