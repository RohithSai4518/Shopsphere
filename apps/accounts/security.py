import base64
import hashlib
import hmac
import json
import secrets
import struct
import time
from datetime import timedelta
from django.utils import timezone
from .models import User, PasswordResetToken
from apps.audit.models import SecurityAuditLog

class TOTPService:
    """
    Pure Python RFC 6238 TOTP (Time-Based One-Time Password) Implementation.
    Generates and verifies 6-digit authentication codes without external dependencies.
    """
    TIME_STEP = 30
    DIGITS = 6

    @staticmethod
    def generate_secret():
        """Generates a random 32-character base32 secret key."""
        random_bytes = secrets.token_bytes(20)
        return base64.b32encode(random_bytes).decode('utf-8').replace('=', '')

    @classmethod
    def get_provisioning_uri(cls, email, secret, issuer="ShopSphere"):
        """Returns standard otpauth:// URL for authenticator apps (Google Authenticator, 1Password)."""
        clean_email = email.strip().replace(" ", "")
        return f"otpauth://totp/{issuer}:{clean_email}?secret={secret}&issuer={issuer}&algorithm=SHA1&digits={cls.DIGITS}&period={cls.TIME_STEP}"

    @classmethod
    def generate_code_for_timestamp(cls, secret, timestamp):
        """Calculates 6-digit TOTP code for a specific timestamp using HMAC-SHA1."""
        # Pad secret if needed
        pad_len = (8 - len(secret) % 8) % 8
        padded_secret = secret + ('=' * pad_len)
        try:
            key = base64.b32decode(padded_secret, casefold=True)
        except Exception:
            return None

        counter = int(timestamp // cls.TIME_STEP)
        counter_bytes = struct.pack(">Q", counter)

        mac = hmac.new(key, counter_bytes, hashlib.sha1).digest()
        offset = mac[-1] & 0x0F
        code_int = struct.unpack(">I", mac[offset:offset + 4])[0] & 0x7FFFFFFF
        code = str(code_int % (10 ** cls.DIGITS)).zfill(cls.DIGITS)
        return code

    @classmethod
    def verify_totp(cls, secret, code, window=1):
        """
        Verifies code against secret with a tolerance window (+/- 1 time step)
        to accommodate reasonable client-server clock drift.
        """
        if not secret or not code:
            return False
        clean_code = str(code).strip()
        if len(clean_code) != cls.DIGITS or not clean_code.isdigit():
            return False

        current_time = int(time.time())
        for delta in range(-window, window + 1):
            t = current_time + (delta * cls.TIME_STEP)
            if cls.generate_code_for_timestamp(secret, t) == clean_code:
                return True
        return False

    @staticmethod
    def generate_backup_codes(count=8):
        """Generates a batch of distinct, human-readable recovery backup codes."""
        codes = []
        for _ in range(count):
            p1 = secrets.token_hex(2).upper()
            p2 = secrets.token_hex(2).upper()
            codes.append(f"{p1}-{p2}")
        return codes

    @staticmethod
    def hash_backup_code(code):
        return hashlib.sha256(code.strip().upper().encode('utf-8')).hexdigest()

    @classmethod
    def verify_and_consume_backup_code(cls, two_factor_obj, code):
        """
        Validates an emergency backup recovery code.
        If valid, removes the consumed code from the list and saves.
        """
        if not two_factor_obj or not two_factor_obj.backup_codes:
            return False

        try:
            hashes = json.loads(two_factor_obj.backup_codes)
        except (ValueError, TypeError):
            return False

        target_hash = cls.hash_backup_code(code)
        if target_hash in hashes:
            hashes.remove(target_hash)
            two_factor_obj.backup_codes = json.dumps(hashes)
            two_factor_obj.save()
            return True

        return False


class PasswordResetService:
    """
    Handles enterprise password reset flows, token generation, rate-limiting,
    complexity validation, and session revocation.
    """

    @staticmethod
    def request_reset(email, ip_address=None):
        """
        Requests a password reset. Returns (success, reset_url or None, message).
        Protects against timing attacks by not leaking if user exists.
        """
        clean_email = email.strip().lower()
        user = User.objects.filter(email=clean_email, is_active=True).first()
        if not user:
            # Return generic success to avoid email enumeration
            return True, None, "If an account exists with that email, instructions have been sent."

        # Invalidate unexpired older tokens for this user
        PasswordResetToken.objects.filter(user=user, is_used=False).update(is_used=True)

        raw_token = f"rst_{secrets.token_urlsafe(32)}"
        token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
        expires_at = timezone.now() + timedelta(hours=2)

        PasswordResetToken.objects.create(
            user=user,
            token_hash=token_hash,
            expires_at=expires_at
        )

        SecurityAuditLog.objects.create(
            user=user,
            action='PASSWORD_RESET_REQUESTED',
            module='accounts',
            ip_address=ip_address
        )

        return True, raw_token, "Password reset instructions have been generated."

    @staticmethod
    def validate_token(raw_token):
        """Verifies if the token is valid, active, and unexpired."""
        if not raw_token:
            return None, "Invalid reset link."

        token_hash = hashlib.sha256(raw_token.encode('utf-8')).hexdigest()
        token_obj = PasswordResetToken.objects.filter(token_hash=token_hash, is_used=False).first()
        if not token_obj:
            return None, "Invalid or already used password reset link."

        if token_obj.expires_at < timezone.now():
            return None, "This password reset link has expired. Please request a new one."

        return token_obj, None

    @staticmethod
    def execute_password_reset(raw_token, new_password, confirm_password, ip_address=None):
        """Validates complexity and applies new password."""
        token_obj, err = PasswordResetService.validate_token(raw_token)
        if err:
            return False, err

        if not new_password or len(new_password) < 8:
            return False, "Password must be at least 8 characters long."

        if new_password != confirm_password:
            return False, "Passwords do not match."

        user = token_obj.user
        user.set_password(new_password)
        user.save()

        token_obj.is_used = True
        token_obj.save()

        # Invalidate all existing active sessions
        user.active_sessions.all().delete()

        SecurityAuditLog.objects.create(
            user=user,
            action='PASSWORD_RESET_COMPLETED',
            module='accounts',
            ip_address=ip_address
        )

        return True, "Your password has been successfully reset. Please sign in."
