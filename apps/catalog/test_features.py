from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product
from apps.catalog.deals import LightningDeal, DealService
from apps.catalog.qa import QAService

User = get_user_model()

class DealsAndQATests(TestCase):
    def setUp(self):
        self.seller_user = User.objects.create_user(
            email='merchant@test.com',
            username='merchant@test.com',
            password='TestPassword123!',
            role='SELLER'
        )
        self.buyer_user = User.objects.create_user(
            email='buyer@test.com',
            username='buyer@test.com',
            password='TestPassword123!',
            role='CUSTOMER'
        )
        self.seller = Seller.objects.create(
            user=self.seller_user,
            business_name='Apex Electronics',
            business_email='merchant@test.com'
        )
        self.category = Category.objects.create(name='Hardware', slug='hardware')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='Precision Ultrabook 14',
            slug='precision-ultrabook-14',
            base_price=Decimal('1200.00'),
            discount_percent=0
        )

    def test_lightning_deal_lifecycle(self):
        now = timezone.now()
        deal = LightningDeal.objects.create(
            product=self.product,
            deal_title='Flash Midnight Deal',
            deal_price=Decimal('899.99'),
            discount_percent=Decimal('25.00'),
            allocated_stock=10,
            starts_at=now - timedelta(minutes=10),
            ends_at=now + timedelta(hours=3),
            is_active=True
        )

        self.assertTrue(deal.is_live)
        self.assertEqual(deal.remaining_units, 10)
        self.assertEqual(deal.discount_percent, Decimal('25.00'))

        # Claim deal
        success, msg = DealService.claim_deal(self.buyer_user, deal.id)
        self.assertTrue(success)
        deal.refresh_from_db()
        self.assertEqual(deal.claimed_units, 1)
        self.assertEqual(deal.remaining_units, 9)

        # Duplicate claim prevention
        second_success, second_msg = DealService.claim_deal(self.buyer_user, deal.id)
        self.assertFalse(second_success)
        self.assertIn("already reserved", second_msg)

    def test_expired_deal_claim_rejection(self):
        now = timezone.now()
        expired_deal = LightningDeal.objects.create(
            product=self.product,
            deal_title='Old Deal',
            deal_price=Decimal('500.00'),
            discount_percent=Decimal('50.00'),
            allocated_stock=5,
            starts_at=now - timedelta(days=2),
            ends_at=now - timedelta(days=1),
            is_active=True
        )
        success, msg = DealService.claim_deal(self.buyer_user, expired_deal.id)
        self.assertFalse(success)
        self.assertIn("not active", msg.lower())

    def test_qa_validation_and_voting(self):
        # Blank question validation
        with self.assertRaises(ValueError):
            QAService.ask_question(self.product, self.buyer_user, "   ")

        question = QAService.ask_question(self.product, self.buyer_user, "Does this unit support USB-C Power Delivery?")
        self.assertEqual(question.question_text, "Does this unit support USB-C Power Delivery?")
        self.assertEqual(question.votes.count(), 0)

        # Merchant answer
        answer = QAService.answer_question(question, self.seller_user, "Yes, up to 100W PD charging is supported.")
        self.assertTrue(answer.is_seller_answer)
        self.assertEqual(answer.votes.count(), 0)

        # Question vote toggle
        voted_added = QAService.vote_question(question, self.buyer_user)
        self.assertTrue(voted_added)
        self.assertEqual(question.votes.count(), 1)

        # Voting again removes vote (toggle)
        voted_removed = QAService.vote_question(question, self.buyer_user)
        self.assertFalse(voted_removed)
        self.assertEqual(question.votes.count(), 0)

        # Answer vote
        vote_obj = QAService.vote_answer(answer, self.buyer_user, is_helpful=True)
        self.assertIsNotNone(vote_obj)
        self.assertEqual(answer.votes.count(), 1)
