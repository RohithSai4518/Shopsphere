import unittest
from unittest import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User, Address, UserSession, UserPreference
from apps.accounts.services import AccountsService

class AccountsModelAndServiceTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user_test@domain.local',
            email='user_test@domain.local',
            password='TestPassword123!',
            first_name='Alex',
            last_name='Tester',
            role='CUSTOMER'
        )

    def test_user_creation_and_preferences(self):
        self.assertEqual(self.user.email, 'user_test@domain.local')
        self.assertTrue(self.user.check_password('TestPassword123!'))
        pref, _ = UserPreference.objects.get_or_create(user=self.user)
        self.assertEqual(pref.currency, 'USD')

    def test_address_default_flag_handling(self):
        addr1 = Address.objects.create(
            user=self.user,
            full_name='Alex Tester',
            street_address_1='100 Tech Blvd',
            city='Austin',
            state='TX',
            postal_code='78701',
            is_default=True
        )
        self.assertTrue(addr1.is_default)

        addr2 = Address.objects.create(
            user=self.user,
            full_name='Alex Office',
            street_address_1='200 Corporate Way',
            city='Austin',
            state='TX',
            postal_code='78702',
            is_default=True
        )

        addr1.refresh_from_db()
        self.assertFalse(addr1.is_default)
        self.assertTrue(addr2.is_default)

    def test_session_creation_and_invalidation(self):
        session, token_str = AccountsService.create_user_session(self.user, ip_address='127.0.0.1')
        self.assertIsNotNone(session.id)
        self.assertEqual(UserSession.objects.filter(user=self.user).count(), 1)

        AccountsService.invalidate_user_sessions(self.user)
        self.assertEqual(UserSession.objects.filter(user=self.user).count(), 0)

    def test_password_reset_token_flow(self):
        reset_obj, raw_token = AccountsService.generate_password_reset_token(self.user)
        self.assertFalse(reset_obj.is_used)

        success, msg = AccountsService.validate_and_use_reset_token(raw_token, 'NewSecurePass456!')
        self.assertTrue(success)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecurePass456!'))
