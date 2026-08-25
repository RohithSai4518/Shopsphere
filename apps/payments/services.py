import random
import uuid
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from .models import Payment, PaymentLedger, PaymentIntent
from apps.audit.models import SecurityAuditLog

class PaymentGatewayError(Exception):
    pass

class PaymentSandboxService:
    @staticmethod
    def create_payment_intent(order):
        intent_token = f"pi_synth_{uuid.uuid4().hex[:16]}"
        expires_at = timezone.now() + timedelta(minutes=30)
        intent = PaymentIntent.objects.create(
            order=order,
            intent_token=intent_token,
            amount=Decimal(str(order.total_amount)),
            status='CREATED',
            expires_at=expires_at
        )
        return intent

    @staticmethod
    def authorize_and_charge(order, payment_method='CREDIT_CARD_SANDBOX'):
        amount = Decimal(str(order.total_amount))
        if amount <= Decimal('0.00'):
            raise PaymentGatewayError("Invalid transaction amount.")

        txn_ref = f"TXN-SANDBOX-{random.randint(1000000, 9999999)}"
        payment = Payment.objects.create(
            order=order,
            payment_method=payment_method,
            transaction_reference=txn_ref,
            amount=amount,
            status='SUCCESS',
            gateway_response_json='{"status": "APPROVED", "code": "00", "gateway": "ShopSphere-Sandbox-PCI"}'
        )

        # Log to ledger
        PaymentLedger.objects.create(
            payment=payment,
            entry_type='AUTHORIZATION',
            amount=amount,
            reference_id=txn_ref
        )
        PaymentLedger.objects.create(
            payment=payment,
            entry_type='CAPTURE',
            amount=amount,
            reference_id=txn_ref
        )

        SecurityAuditLog.objects.create(
            user=order.user,
            action='PAYMENT_SUCCESS',
            module='payments',
            entity_type='Payment',
            entity_id=payment.id,
            metadata_json=f'{{"amount": {amount}, "ref": "{txn_ref}"}}'
        )

        return payment

    @staticmethod
    def process_refund(payment, refund_amount):
        refund_dec = Decimal(str(refund_amount))
        if refund_dec > payment.amount:
            raise PaymentGatewayError("Refund amount cannot exceed original transaction charge.")

        if refund_dec == payment.amount:
            payment.status = 'REFUNDED'
        else:
            payment.status = 'PARTIALLY_REFUNDED'

        payment.save()

        # Log refund in ledger
        PaymentLedger.objects.create(
            payment=payment,
            entry_type='REFUND',
            amount=refund_dec,
            reference_id=f"REF-{uuid.uuid4().hex[:8]}"
        )

        SecurityAuditLog.objects.create(
            user=payment.order.user,
            action='PAYMENT_REFUND',
            module='payments',
            entity_type='Payment',
            entity_id=payment.id,
            metadata_json=f'{{"refund_amount": {refund_dec}}}'
        )

        return payment
