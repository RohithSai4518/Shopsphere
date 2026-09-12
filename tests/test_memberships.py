import unittest
from unittest import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant
from apps.orders.models import Order
from apps.memberships.models import (
    MembershipTier, UserMembership, RewardWallet,
    RewardTransaction, SubscriptionPlan
)
from apps.memberships.services import MembershipService, RewardWalletService

class MembershipsSubsystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='prime_member@example.com',
            email='prime_member@example.com',
            password='Password123!'
        )
        self.seller = Seller.objects.create(
            user=self.user,
            business_name='Coffee Roast Co',
            business_email='coffee@example.com',
            status='APPROVED'
        )
        self.tier = MembershipTier.objects.create(
            tier_code='MONTHLY_PRIME',
            name='ShopSphere Prime Monthly',
            price=Decimal('14.99'),
            billing_period_days=30,
            cashback_reward_pct=Decimal('5.00')
        )
        self.category = Category.objects.create(name='Coffee & Pantry', slug='coffee-pantry')
        self.product = Product.objects.create(
            name='Organic Dark Roast Coffee Beans',
            slug='organic-dark-roast',
            category=self.category,
            seller=self.seller,
            base_price=Decimal('20.00'),
            status='PUBLISHED'
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='COFFEE-DR-01',
            variant_name='12 oz Bag',
            price_override=Decimal('20.00')
        )
        self.order = Order.objects.create(
            order_number='ORD-MEM-1001',
            user=self.user,
            status='CONFIRMED',
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('8.00'),
            shipping_amount=Decimal('0.00'),
            total_amount=Decimal('108.00')
        )

    def test_prime_enrollment_and_welcome_bonus(self):
        membership = MembershipService.enroll_user(self.user, 'MONTHLY_PRIME')
        self.assertEqual(membership.status, 'ACTIVE')
        self.assertTrue(MembershipService.is_user_prime(self.user))

        # Check welcome bonus points (500 pts = $5.00)
        wallet = self.user.reward_wallet
        self.assertEqual(wallet.points_balance, 500)
        self.assertEqual(wallet.cash_value, Decimal('5.00'))

    def test_rewards_accrual_standard_vs_prime(self):
        # 1. Standard non-prime user earns 2%
        user2 = User.objects.create_user(username='standard@example.com', email='standard@example.com', password='Password123!')
        order2 = Order.objects.create(
            order_number='ORD-MEM-1002',
            user=user2,
            status='CONFIRMED',
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('8.00'),
            shipping_amount=Decimal('5.00'),
            total_amount=Decimal('113.00')
        )
        tx2 = RewardWalletService.accrue_points_for_order(order2)
        # 2% of $100 = $2.00 -> 200 points
        self.assertEqual(tx2.points, 200)
        self.assertEqual(tx2.transaction_type, 'PURCHASE_EARN')

        # 2. Prime user earns 5%
        MembershipService.enroll_user(self.user, 'MONTHLY_PRIME')
        tx_prime = RewardWalletService.accrue_points_for_order(self.order)
        # 5% of $100 = $5.00 -> 500 points
        self.assertEqual(tx_prime.points, 500)
        self.assertEqual(tx_prime.transaction_type, 'PRIME_BONUS')

    def test_rewards_redemption(self):
        wallet = RewardWalletService.get_or_create_wallet(self.user)
        wallet.points_balance = 1000
        wallet.save()

        success, discount = RewardWalletService.redeem_points(self.user, 500, self.order)
        self.assertTrue(success)
        self.assertEqual(discount, Decimal('5.00'))
        wallet.refresh_from_db()
        self.assertEqual(wallet.points_balance, 500)
        self.assertEqual(wallet.lifetime_points_redeemed, 500)

    def test_subscribe_and_save_flow(self):
        sub = SubscriptionPlan.objects.create(
            user=self.user,
            variant=self.variant,
            quantity=2,
            frequency_months=1,
            discount_percentage=Decimal('5.00'),
            status='ACTIVE',
            next_delivery_date=timezone.now().date() + timedelta(days=30)
        )
        self.assertEqual(sub.status, 'ACTIVE')

        # Test toggle views
        self.client.force_login(self.user)
        resp = self.client.post(reverse('memberships:toggle_subscription', args=[sub.id]), {'action': 'pause'})
        self.assertEqual(resp.status_code, 302)
        sub.refresh_from_db()
        self.assertEqual(sub.status, 'PAUSED')

    def test_prime_and_wallet_views(self):
        self.client.force_login(self.user)
        resp_prime = self.client.get(reverse('memberships:prime_landing'))
        self.assertEqual(resp_prime.status_code, 200)
        self.assertContains(resp_prime, 'ShopSphere Prime')

        resp_wallet = self.client.get(reverse('memberships:wallet'))
        self.assertEqual(resp_wallet.status_code, 200)
        self.assertContains(resp_wallet, 'Reward Points & Wallet')
