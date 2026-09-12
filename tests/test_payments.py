import unittest
from unittest import TestCase
from decimal import Decimal
from django.contrib.auth import get_user_model
from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.services import PaymentSandboxService, PaymentGatewayError

User = get_user_model()

class PaymentsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='pay_user@example.com', username='pay_user@example.com', password='Password123!')
        self.order = Order.objects.create(
            order_number='ORD-PAY-1',
            user=self.user,
            subtotal=Decimal('100.00'),
            tax_amount=Decimal('8.25'),
            shipping_amount=Decimal('0.00'),
            total_amount=Decimal('108.25')
        )

    def test_payment_sandbox_charge(self):
        payment = PaymentSandboxService.authorize_and_charge(self.order)
        self.assertEqual(payment.amount, Decimal('108.25'))
        self.assertEqual(payment.status, 'SUCCESS')

    def test_payment_sandbox_refund(self):
        payment = PaymentSandboxService.authorize_and_charge(self.order)
        refunded = PaymentSandboxService.process_refund(payment, Decimal('50.00'))
        self.assertEqual(refunded.status, 'PARTIALLY_REFUNDED')
