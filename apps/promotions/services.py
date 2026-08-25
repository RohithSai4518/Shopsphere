from django.utils import timezone
from decimal import Decimal
import hashlib, uuid
from .models import Coupon, CouponUsage, GiftCard
from apps.audit.models import SecurityAuditLog

class CouponValidationError(Exception):
    pass

class PromotionService:
    @staticmethod
    def validate_and_apply_coupon(code, subtotal, user=None, seller=None, category=None):
        coupon = Coupon.objects.filter(code__iexact=code, is_active=True).first()
        if not coupon:
            raise CouponValidationError(f"Invalid or expired promotional coupon code: '{code}'.")

        now = timezone.now()
        if coupon.starts_at > now or coupon.expires_at < now:
            raise CouponValidationError("This promotional coupon has expired.")

        subtotal_dec = Decimal(str(subtotal))
        if subtotal_dec < coupon.min_order_subtotal:
            raise CouponValidationError(f"Coupon requires a minimum order subtotal of ${coupon.min_order_subtotal}.")

        if coupon.seller and seller and coupon.seller != seller:
            raise CouponValidationError("This coupon is restricted to specific seller products.")

        if coupon.category and category and coupon.category != category:
            raise CouponValidationError("This coupon is restricted to specific product categories.")

        # Per-user limit check
        if user and user.is_authenticated:
            user_uses = CouponUsage.objects.filter(coupon=coupon, user=user).count()
            if user_uses >= coupon.per_user_limit:
                raise CouponValidationError("You have already reached the maximum usage limit for this coupon.")

        # Total usage limit check
        if coupon.redemptions.count() >= coupon.usage_limit:
            raise CouponValidationError("This promotional coupon usage limit has been reached.")

        discount = coupon.calculate_discount(subtotal_dec)
        return coupon, discount

    @staticmethod
    def record_coupon_redemption(coupon, user, discount_applied, order_id=None):
        usage = CouponUsage.objects.create(
            coupon=coupon,
            user=user,
            order_id=order_id,
            discount_applied=Decimal(str(discount_applied))
        )
        return usage

    @staticmethod
    def create_gift_card(initial_balance, duration_days=365):
        raw_code = f"GC-{uuid.uuid4().hex[:12].upper()}"
        expires_at = timezone.now() + timezone.timedelta(days=duration_days)
        gift_card = GiftCard.objects.create(
            code=raw_code,
            initial_balance=Decimal(str(initial_balance)),
            current_balance=Decimal(str(initial_balance)),
            expires_at=expires_at,
            is_active=True
        )
        return gift_card

    @staticmethod
    def redeem_gift_card(code, amount_to_apply):
        gc = GiftCard.objects.filter(code__iexact=code, is_active=True).first()
        if not gc:
            raise CouponValidationError("Invalid or inactive gift card code.")

        if gc.expires_at < timezone.now():
            raise CouponValidationError("This gift card has expired.")

        apply_dec = Decimal(str(amount_to_apply))
        if gc.current_balance < apply_dec:
            applied = gc.current_balance
            gc.current_balance = Decimal('0.00')
        else:
            applied = apply_dec
            gc.current_balance -= apply_dec

        gc.save()
        return applied
