from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant
from apps.inventory.services import InventoryService
from apps.cart.models import CartItem
from apps.orders.models import Order
from apps.orders.services import OrderService
from apps.orders.invoicing import InvoiceService

User = get_user_model()

class CheckoutPipelineAndInvoicingTests(TestCase):
    def setUp(self):
        self.seller_user = User.objects.create_user(
            email='vendor@test.com',
            username='vendor@test.com',
            password='TestPassword123!',
            role='SELLER'
        )
        self.buyer_user = User.objects.create_user(
            email='customer@test.com',
            username='customer@test.com',
            password='TestPassword123!',
            role='CUSTOMER'
        )
        self.seller = Seller.objects.create(
            user=self.seller_user,
            business_name='NexGen Store',
            business_email='vendor@test.com'
        )
        self.category = Category.objects.create(name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='Noise-Cancelling Wireless Headphones',
            slug='noise-cancelling-headphones',
            base_price=Decimal('200.00'),
            discount_percent=0
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='NCH-BLK-01',
            variant_name='Midnight Black',
            price_override=Decimal('200.00')
        )
        InventoryService.restock_variant(self.variant, 50, notes='Initial Test Restock')

    def test_checkout_with_idempotency_and_invoicing(self):
        cart_item = CartItem.objects.create(
            user=self.buyer_user,
            variant=self.variant,
            quantity=2
        )
        cart_items = CartItem.objects.filter(user=self.buyer_user)
        shipping_json = '{"full_name": "Customer One", "street": "100 Innovation Blvd", "city": "San Francisco", "state": "CA", "postal_code": "94105"}'

        idempotency_key = "idemp_test_unique_key_001"

        order = OrderService.process_checkout(
            user=self.buyer_user,
            cart_items=cart_items,
            shipping_address=shipping_json,
            delivery_speed='EXPEDITED',
            is_gift=True,
            gift_message="Happy Birthday Alex!",
            gift_wrap_type='DELUXE',
            idempotency_key=idempotency_key
        )

        self.assertIsNotNone(order)
        self.assertEqual(order.delivery_speed, 'EXPEDITED')
        self.assertEqual(order.shipping_amount, Decimal('9.99'))
        self.assertTrue(order.is_gift)
        self.assertEqual(order.gift_wrap_fee, Decimal('7.99'))
        self.assertEqual(order.gift_message, "Happy Birthday Alex!")

        # Automated Tax Invoice generation verification
        self.assertTrue(hasattr(order, 'invoice'))
        invoice = order.invoice
        self.assertTrue(invoice.invoice_number.startswith('INV-'))
        self.assertEqual(invoice.total_amount, order.total_amount)

        # Idempotency double-submit check
        # Attempt to process checkout again with identical idempotency key
        duplicate_attempt = OrderService.process_checkout(
            user=self.buyer_user,
            cart_items=cart_items,
            shipping_address=shipping_json,
            idempotency_key=idempotency_key
        )
        self.assertEqual(duplicate_attempt.id, order.id)
        self.assertEqual(Order.objects.filter(user=self.buyer_user).count(), 1)
