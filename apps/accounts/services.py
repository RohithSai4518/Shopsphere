import hashlib
import uuid
from django.utils import timezone
from datetime import timedelta
from .models import User, UserSession, LoginHistory, UserPreference, PasswordResetToken, SavedPaymentMethod
from apps.audit.models import SecurityAuditLog

class AccountsService:
    @staticmethod
    def create_user_session(user, ip_address=None, user_agent=None, duration_days=7):
        token_str = f"{user.id}-{uuid.uuid4().hex}"
        token_hash = hashlib.sha256(token_str.encode('utf-8')).hexdigest()
        expires_at = timezone.now() + timedelta(days=duration_days)

        session = UserSession.objects.create(
            user=user,
            token_hash=token_hash,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at
        )

        LoginHistory.objects.create(
            user=user,
            ip_address=ip_address,
            user_agent=user_agent,
            status='SUCCESS'
        )

        SecurityAuditLog.objects.create(
            user=user,
            action='USER_LOGIN_SUCCESS',
            module='accounts',
            ip_address=ip_address,
            metadata_json=f'{{"session_id": "{session.id}"}}'
        )

        return session, token_str

    @staticmethod
    def generate_password_reset_token(user):
        raw_token = f"rst-{user.id}-{uuid.uuid4().hex}"
        token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
        expires_at = timezone.now() + timedelta(hours=24)

        reset_token = PasswordResetToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at
        )
        return reset_token, raw_token

    @staticmethod
    def validate_and_use_reset_token(raw_token, new_password):
        token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
        token = PasswordResetToken.objects.filter(token_hash=token_hash, is_used=False).first()
        if not token:
            return False, "Invalid or expired password reset token."

        if token.expires_at < timezone.now():
            return False, "Password reset token has expired."

        user = token.user
        user.set_password(new_password)
        user.save()

        token.is_used = True
        token.save()

        # Invalidate existing active sessions for security
        AccountsService.invalidate_user_sessions(user)

        SecurityAuditLog.objects.create(
            user=user,
            action='PASSWORD_RESET_SUCCESS',
            module='accounts'
        )

        return True, "Password reset successfully."

    @staticmethod
    def invalidate_user_sessions(user):
        return UserSession.objects.filter(user=user).delete()

    @staticmethod
    def add_saved_payment_method(user, card_brand, last4, expiry_month, expiry_year, is_default=False):
        gateway_token_ref = f"tok_synth_{uuid.uuid4().hex[:12]}"
        return SavedPaymentMethod.objects.create(
            user=user,
            card_brand=card_brand,
            last4=last4,
            expiry_month=expiry_month,
            expiry_year=expiry_year,
            gateway_token_ref=gateway_token_ref,
            is_default=is_default
        )
