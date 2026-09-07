import time
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import UserTwoFactor
from apps.accounts.security import TOTPService, PasswordResetService
from apps.accounts.privacy import PrivacyService

User = get_user_model()

class AccountsSecurityAndPrivacyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='alice@example.com',
            username='alice@example.com',
            password='InitialPassword123!',
            first_name='Alice',
            last_name='Smith'
        )

    def test_totp_rfc6238_generation_and_verification(self):
        secret = TOTPService.generate_secret()
        self.assertGreaterEqual(len(secret), 16)

        # Generate code for current timestamp
        current_time = time.time()
        code = TOTPService.generate_code_for_timestamp(secret, current_time)
        self.assertEqual(len(code), 6)
        self.assertTrue(code.isdigit())

        # Verify correct code
        self.assertTrue(TOTPService.verify_totp(secret, code))

        # Incorrect code rejection
        self.assertFalse(TOTPService.verify_totp(secret, '999999'))
        self.assertFalse(TOTPService.verify_totp(secret, 'abc'))

    def test_backup_recovery_codes_consumption(self):
        two_factor = UserTwoFactor.objects.create(
            user=self.user,
            is_enabled=True,
            secret_key=TOTPService.generate_secret()
        )
        codes = TOTPService.generate_backup_codes(8)
        self.assertEqual(len(codes), 8)

        # Save hashed backup codes
        import json
        hashed = [TOTPService.hash_backup_code(c) for c in codes]
        two_factor.backup_codes = json.dumps(hashed)
        two_factor.save()

        # Redeem first code
        consumed = TOTPService.verify_and_consume_backup_code(two_factor, codes[0])
        self.assertTrue(consumed)
        two_factor.refresh_from_db()
        remaining_hashes = json.loads(two_factor.backup_codes)
        self.assertEqual(len(remaining_hashes), 7)

        # Re-using already consumed code must fail
        consumed_again = TOTPService.verify_and_consume_backup_code(two_factor, codes[0])
        self.assertFalse(consumed_again)

    def test_password_reset_flow(self):
        success, raw_token, msg = PasswordResetService.request_reset('alice@example.com')
        self.assertTrue(success)
        self.assertIsNotNone(raw_token)

        # Confirm reset with weak password
        ok, err = PasswordResetService.execute_password_reset(raw_token, 'short', 'short')
        self.assertFalse(ok)
        self.assertIn("at least 8 characters", err)

        # Confirm reset with valid password
        ok, msg = PasswordResetService.execute_password_reset(raw_token, 'NewSecurePassword2026!', 'NewSecurePassword2026!')
        self.assertTrue(ok)

        # Verify user can authenticate with new password
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewSecurePassword2026!'))

    def test_gdpr_data_portability_and_erasure(self):
        archive = PrivacyService.generate_full_data_archive(self.user)
        self.assertEqual(archive['profile']['email'], 'alice@example.com')
        self.assertIn('gdpr_export_metadata', archive)
        self.assertIn('orders', archive)
        self.assertIn('addresses', archive)

        # Execute Right to Erasure
        erased, msg = PrivacyService.execute_right_to_be_forgotten(self.user)
        self.assertTrue(erased)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(self.user.status, 'ERASED')
        self.assertTrue(self.user.email.startswith('erased_'))
