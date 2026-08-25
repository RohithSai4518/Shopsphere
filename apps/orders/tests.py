from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant
from apps.orders.models import Order, OrderItem
from .tests_expanded import CartAndCheckoutExpandedTestSuite

User = get_user_model()

class OrdersModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='buyer@example.com',
            username='buyer@example.com',
            password='BuyerPassword123!'
        )
        self.seller_user = User.objects.create_user(
            email='merchant3@example.com',
            username='merchant3@example.com',
            password='MerchantPassword123!',
            role='SELLER'
        )
        self.seller = Seller.objects.create(user=self.seller_user, business_name='Merchant 3', business_email='merchant3@example.com')
        self.category = Category.objects.create(name='Audio', slug='audio')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='Headphones',
            slug='headphones',
            base_price=100.00
        )
        self.variant = ProductVariant.objects.create(product=self.product, sku='HP-01', variant_name='Black')

    def test_order_creation_and_item_linkage(self):
        order = Order.objects.create(
            order_number='ORD-TEST-100',
            user=self.user,
            subtotal=100.00,
            tax_amount=8.25,
            shipping_amount=0.00,
            total_amount=108.25
        )
        item = OrderItem.objects.create(
            order=order,
            variant=self.variant,
            seller=self.seller,
            unit_price=100.00,
            quantity=1,
            total_price=100.00
        )
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(item.order.order_number, 'ORD-TEST-100')

class FullCartAndCheckoutExpandedTests(CartAndCheckoutExpandedTestSuite):
    pass
