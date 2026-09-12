from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from .models import (
    MembershipTier, UserMembership, RewardWallet,
    RewardTransaction, SubscriptionPlan, SubscriptionExecutionLog
)

class MembershipService:
    """
    Manages Prime membership status, benefit verification, and tier upgrades.
    """

    @classmethod
    def is_user_prime(cls, user):
        if not user or not user.is_authenticated:
            return False
        membership = UserMembership.objects.filter(user=user, status='ACTIVE').first()
        return bool(membership and membership.is_valid)

    @classmethod
    def get_user_tier(cls, user):
        if not user or not user.is_authenticated:
            return None
        membership = UserMembership.objects.filter(user=user, status='ACTIVE').select_related('tier').first()
        if membership and membership.is_valid:
            return membership.tier
        return None

    @classmethod
    @transaction.atomic
    def enroll_user(cls, user, tier_code='MONTHLY_PRIME'):
        tier = MembershipTier.objects.filter(tier_code=tier_code, is_active=True).first()
        if not tier:
            tier, _ = MembershipTier.objects.get_or_create(
                tier_code='MONTHLY_PRIME',
                defaults={
                    'name': 'ShopSphere Prime (Monthly)',
                    'price': Decimal('14.99'),
                    'billing_period_days': 30,
                    'cashback_reward_pct': Decimal('5.00')
                }
            )

        now = timezone.now()
        end_time = now + timedelta(days=tier.billing_period_days)

        membership, created = UserMembership.objects.get_or_create(
            user=user,
            defaults={'tier': tier, 'end_date': end_time, 'status': 'ACTIVE', 'auto_renew': True}
        )
        if not created:
            membership.tier = tier
            membership.end_date = end_time
            membership.status = 'ACTIVE'
            membership.auto_renew = True
            membership.save()

        # Bonus 500 welcome points to reward wallet
        RewardWalletService.credit_bonus_points(user, 500, "Welcome bonus for joining ShopSphere Prime!")
        return membership


class RewardWalletService:
    """
    Manages reward points accrual (cashback) and redemption during checkout.
    """

    @classmethod
    def get_or_create_wallet(cls, user):
        wallet, _ = RewardWallet.objects.get_or_create(user=user)
        return wallet

    @classmethod
    @transaction.atomic
    def accrue_points_for_order(cls, order):
        user = order.user
        wallet = cls.get_or_create_wallet(user)
        is_prime = MembershipService.is_user_prime(user)

        # Standard 2% back, Prime 5% back
        rate = Decimal('0.05') if is_prime else Decimal('0.02')
        earned_dollars = round(order.subtotal * rate, 2)
        earned_points = int(earned_dollars * Decimal('100.00'))

        if earned_points <= 0:
            return None

        wallet.points_balance += earned_points
        wallet.lifetime_points_earned += earned_points
        wallet.save()

        tx_type = 'PRIME_BONUS' if is_prime else 'PURCHASE_EARN'
        desc = f"{'Prime 5%' if is_prime else 'Standard 2%'} reward points on Order #{order.order_number}"

        tx = RewardTransaction.objects.create(
            wallet=wallet,
            order=order,
            transaction_type=tx_type,
            points=earned_points,
            cash_equivalent=earned_dollars,
            balance_after=wallet.points_balance,
            description=desc
        )
        return tx

    @classmethod
    @transaction.atomic
    def redeem_points(cls, user, points_to_redeem, order=None):
        wallet = cls.get_or_create_wallet(user)
        if points_to_redeem <= 0 or points_to_redeem > wallet.points_balance:
            return False, "Insufficient reward points balance."

        cash_val = round(Decimal(points_to_redeem) / Decimal('100.00'), 2)
        wallet.points_balance -= points_to_redeem
        wallet.lifetime_points_redeemed += points_to_redeem
        wallet.save()

        tx = RewardTransaction.objects.create(
            wallet=wallet,
            order=order,
            transaction_type='CHECKOUT_REDEEM',
            points=-points_to_redeem,
            cash_equivalent=cash_val,
            balance_after=wallet.points_balance,
            description=f"Redeemed {points_to_redeem} points for ${cash_val:.2f} discount."
        )
        return True, cash_val

    @classmethod
    @transaction.atomic
    def credit_bonus_points(cls, user, points, description):
        wallet = cls.get_or_create_wallet(user)
        wallet.points_balance += points
        wallet.lifetime_points_earned += points
        wallet.save()

        cash_val = round(Decimal(points) / Decimal('100.00'), 2)
        return RewardTransaction.objects.create(
            wallet=wallet,
            transaction_type='PROMO_GIFT',
            points=points,
            cash_equivalent=cash_val,
            balance_after=wallet.points_balance,
            description=description
        )
