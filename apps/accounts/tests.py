from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import Address, UserPreference

User = get_user_model()

class AccountsModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            username='testuser@example.com',
            password='TestPassword123!',
            first_name='Test',
            last_name='User',
            role='CUSTOMER'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertTrue(self.user.check_password('TestPassword123!'))
        self.assertEqual(self.user.role, 'CUSTOMER')

    def test_address_default_flag(self):
        addr1 = Address.objects.create(
            user=self.user,
            full_name='Test User',
            street_address_1='123 Main St',
            city='San Francisco',
            state='CA',
            postal_code='94105',
            is_default=True
        )
        self.assertTrue(addr1.is_default)

        addr2 = Address.objects.create(
            user=self.user,
            full_name='Test User Work',
            street_address_1='456 Market St',
            city='San Francisco',
            state='CA',
            postal_code='94105',
            is_default=True
        )
        addr1.refresh_from_db()
        self.assertFalse(addr1.is_default)
        self.assertTrue(addr2.is_default)
