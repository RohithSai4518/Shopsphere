import unittest
from unittest import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone
from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant
from apps.orders.models import Order, OrderItem
from apps.payouts.models import (
    SellerEscrowAccount, EscrowTransaction, PayoutBatch,
    PayoutItem, SellerCommissionRule, SellerBankAccount
)
from apps.payouts.services import EscrowService, SettlementBatchService

class PayoutsSubsystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.seller_user = User.objects.create_user(
            username='merchant_test@shopsphere.local',
            email='merchant_test@shopsphere.local',
            password='Password123!',
            role='SELLER'
        )
        self.seller = Seller.objects.create(
            user=self.seller_user,
            business_name='Apex Gadgets Direct',
            business_email='apex@example.com',
            commission_rate=Decimal('10.00'),
            status='APPROVED'
        )
        self.buyer = User.objects.create_user(
            username='shopper_payout@example.com',
            email='shopper_payout@example.com',
            password='Password123!'
        )
        self.category = Category.objects.create(name='Electronics', slug='electronics-payout')
        self.comm_rule = SellerCommissionRule.objects.create(
            category=self.category,
            tier_name='Electronics 8% Platform Fee',
            fee_percentage=Decimal('8.00'),
            minimum_fee=Decimal('1.00')
        )
        self.product = Product.objects.create(
            name='Wireless Noise-Cancelling Headphones',
            slug='wireless-anc-headphones',
            category=self.category,
            seller=self.seller,
            base_price=Decimal('200.00'),
            status='PUBLISHED'
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='ANC-HEAD-01',
            variant_name='Black',
            price_override=Decimal('200.00')
        )
        self.bank = SellerBankAccount.objects.create(
            seller=self.seller,
            bank_name='Silicon Valley Bank',
            account_holder_name='Apex Gadgets LLC',
            routing_number='121000358',
            account_number_last4='9081',
            is_primary=True,
            is_verified=True
        )
        self.order = Order.objects.create(
            order_number='ORD-PAY-8822',
            user=self.buyer,
            status='CONFIRMED',
            subtotal=Decimal('200.00'),
            tax_amount=Decimal('16.00'),
            shipping_amount=Decimal('0.00'),
            total_amount=Decimal('216.00')
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            variant=self.variant,
            seller=self.seller,
            unit_price=Decimal('200.00'),
            quantity=1,
            total_price=Decimal('200.00')
        )

    def test_escrow_holding_and_commission_calculation(self):
        txs = EscrowService.hold_order_payment(self.order)
        self.assertEqual(len(txs), 1)
        tx = txs[0]

        # 8% on $200 = $16 commission -> net $184 held
        self.assertEqual(tx.gross_amount, Decimal('200.00'))
        self.assertEqual(tx.commission_fee, Decimal('16.00'))
        self.assertEqual(tx.net_amount, Decimal('184.00'))
        self.assertFalse(tx.is_released)

        account = self.seller.escrow_account
        self.assertEqual(account.pending_balance, Decimal('184.00'))
        self.assertEqual(account.available_balance, Decimal('0.00'))

    def test_escrow_funds_release_after_return_period(self):
        EscrowService.hold_order_payment(self.order)
        account = self.seller.escrow_account

        # Manually mature the transaction
        EscrowTransaction.objects.filter(account=account).update(
            release_eligible_at=timezone.now() - timedelta(days=1)
        )

        released_count, total_released = EscrowService.release_eligible_funds()
        self.assertEqual(released_count, 1)
        self.assertEqual(total_released, Decimal('184.00'))

        account.refresh_from_db()
        self.assertEqual(account.pending_balance, Decimal('0.00'))
        self.assertEqual(account.available_balance, Decimal('184.00'))

    def test_batch_settlement_generation_and_execution(self):
        account = EscrowService.get_or_create_account(self.seller)
        account.available_balance = Decimal('500.00')
        account.save()

        today = date.today()
        batch = SettlementBatchService.create_payout_batch(today - timedelta(days=14), today)
        self.assertEqual(batch.total_sellers_count, 1)
        self.assertEqual(batch.total_net_disbursed, Decimal('500.00'))

        # Execute batch
        success = SettlementBatchService.execute_batch(batch)
        self.assertTrue(success)
        self.assertEqual(batch.status, 'COMPLETED')

        account.refresh_from_db()
        self.assertEqual(account.available_balance, Decimal('0.00'))
        self.assertEqual(account.lifetime_payouts, Decimal('500.00'))

    def test_seller_dashboard_and_statement_views(self):
        self.client.force_login(self.seller_user)
        resp = self.client.get(reverse('payouts:dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Apex Gadgets Direct')

        # Test CSV export
        today = date.today()
        batch = SettlementBatchService.create_payout_batch(today - timedelta(days=14), today)
        csv_resp = self.client.get(reverse('payouts:statement_detail', args=[batch.id]) + '?format=csv')
        self.assertEqual(csv_resp.status_code, 200)
        self.assertEqual(csv_resp['Content-Type'], 'text/csv')
