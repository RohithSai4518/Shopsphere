import uuid
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.db import transaction
from .models import (
    SellerEscrowAccount, EscrowTransaction, PayoutBatch,
    PayoutItem, SellerCommissionRule, SellerBankAccount
)
from apps.sellers.models import Seller
from apps.orders.models import Order

class EscrowService:
    """
    Manages seller escrow balances, holding gross payments until the return period
    has elapsed (e.g. 14 days post-delivery) to protect buyers and prevent negative balances.
    """

    @classmethod
    def get_or_create_account(cls, seller):
        account, _ = SellerEscrowAccount.objects.get_or_create(seller=seller)
        return account

    @classmethod
    @transaction.atomic
    def hold_order_payment(cls, order):
        """
        Calculates commission and credits seller escrow pending balance when an order is paid.
        """
        # Group order items by seller
        seller_totals = {}
        for item in order.items.select_related('variant__product__category', 'seller'):
            s = item.seller
            if s not in seller_totals:
                seller_totals[s] = {'gross': Decimal('0.00'), 'commission': Decimal('0.00')}

            gross = item.total_price
            # Look up commission rule for item's category
            cat = item.variant.product.category if item.variant and item.variant.product else None
            rule = SellerCommissionRule.objects.filter(category=cat, is_active=True).first()
            if not rule:
                rule = SellerCommissionRule.objects.filter(category=None, is_active=True).first()

            pct = rule.fee_percentage if rule else Decimal('10.00')
            min_fee = rule.minimum_fee if rule else Decimal('0.50')
            fee = max(round(gross * (pct / Decimal('100.00')), 2), min_fee)

            seller_totals[s]['gross'] += gross
            seller_totals[s]['commission'] += fee

        transactions_created = []
        release_date = timezone.now() + timedelta(days=14)

        for seller, totals in seller_totals.items():
            account = cls.get_or_create_account(seller)
            net = totals['gross'] - totals['commission']

            etx = EscrowTransaction.objects.create(
                account=account,
                order=order,
                transaction_type='ORDER_HOLD',
                gross_amount=totals['gross'],
                commission_fee=totals['commission'],
                net_amount=net,
                release_eligible_at=release_date,
                is_released=False,
                notes=f"Held in escrow for Order #{order.order_number}. Eligible for release on {release_date.strftime('%Y-%m-%d')}."
            )
            account.pending_balance += net
            account.lifetime_earnings += net
            account.save()
            transactions_created.append(etx)

        return transactions_created

    @classmethod
    @transaction.atomic
    def release_eligible_funds(cls):
        """
        Releases pending escrow transactions whose return window has passed into available balance.
        """
        now = timezone.now()
        mature_txs = EscrowTransaction.objects.filter(
            transaction_type='ORDER_HOLD',
            is_released=False,
            release_eligible_at__lte=now
        ).select_related('account')

        released_count = 0
        total_released = Decimal('0.00')

        for etx in mature_txs:
            account = etx.account
            # Shift from pending to available
            account.pending_balance = max(Decimal('0.00'), account.pending_balance - etx.net_amount)
            account.available_balance += etx.net_amount
            account.save()

            etx.is_released = True
            etx.save()

            # Record ledger release transaction
            EscrowTransaction.objects.create(
                account=account,
                order=etx.order,
                transaction_type='RETURN_WINDOW_RELEASE',
                gross_amount=etx.gross_amount,
                commission_fee=etx.commission_fee,
                net_amount=etx.net_amount,
                is_released=True,
                notes=f"Funds released from escrow hold for Order #{etx.order.order_number if etx.order else 'N/A'}."
            )
            released_count += 1
            total_released += etx.net_amount

        return released_count, total_released


class SettlementBatchService:
    """
    Executes scheduled payout batches, transferring available balances to verified seller bank accounts.
    """

    @classmethod
    @transaction.atomic
    def create_payout_batch(cls, cycle_start, cycle_end):
        batch_ref = f"PAY-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        batch = PayoutBatch.objects.create(
            batch_reference=batch_ref,
            cycle_start=cycle_start,
            cycle_end=cycle_end,
            status='DRAFT'
        )

        eligible_accounts = SellerEscrowAccount.objects.filter(
            available_balance__gt=Decimal('10.00'), # $10 minimum payout threshold
            is_payout_hold=False
        ).select_related('seller')

        total_gross = Decimal('0.00')
        total_comm = Decimal('0.00')
        total_net = Decimal('0.00')
        sellers_count = 0

        for account in eligible_accounts:
            bank = SellerBankAccount.objects.filter(seller=account.seller, is_verified=True, is_primary=True).first()
            amount_to_payout = account.available_balance

            PayoutItem.objects.create(
                batch=batch,
                seller=account.seller,
                bank_account=bank,
                gross_sales=amount_to_payout,
                platform_fee=Decimal('0.00'),
                net_payout=amount_to_payout,
                is_settled=False,
                transfer_reference=f"ACH-{uuid.uuid4().hex[:8].upper()}"
            )

            total_net += amount_to_payout
            total_gross += amount_to_payout
            sellers_count += 1

        batch.total_sellers_count = sellers_count
        batch.total_gross_revenue = total_gross
        batch.total_net_disbursed = total_net
        batch.save()
        return batch

    @classmethod
    @transaction.atomic
    def execute_batch(cls, batch):
        if batch.status == 'COMPLETED':
            return False

        for item in batch.items.select_related('seller__escrow_account'):
            seller = item.seller
            account = seller.escrow_account
            account.available_balance = max(Decimal('0.00'), account.available_balance - item.net_payout)
            account.lifetime_payouts += item.net_payout
            account.save()

            EscrowTransaction.objects.create(
                account=account,
                transaction_type='PAYOUT_SETTLEMENT',
                gross_amount=item.net_payout,
                net_amount=-item.net_payout,
                is_released=True,
                notes=f"Disbursed via Batch {batch.batch_reference} (Ref: {item.transfer_reference})"
            )
            item.is_settled = True
            item.save()

        batch.status = 'COMPLETED'
        batch.executed_at = timezone.now()
        batch.save()
        return True
