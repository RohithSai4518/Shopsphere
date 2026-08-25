from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant
from apps.orders.models import Order, OrderItem
from apps.returns.models import ReturnRequest

User = get_user_model()

class ReturnsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='ret_user@example.com', username='ret_user@example.com', password='Pass')
        self.seller_user = User.objects.create_user(email='ret_sel@example.com', username='ret_sel@example.com', password='Pass', role='SELLER')
        self.seller = Seller.objects.create(user=self.seller_user, business_name='Seller R', business_email='ret_sel@example.com')
        self.cat = Category.objects.create(name='Cat', slug='cat')
        self.product = Product.objects.create(seller=self.seller, category=self.cat, name='Prod', slug='prod', base_price=50.00)
        self.variant = ProductVariant.objects.create(product=self.product, sku='SKU-R', variant_name='Var')
        self.order = Order.objects.create(order_number='ORD-RET-1', user=self.user, subtotal=50.00, tax_amount=4.00, shipping_amount=0.00, total_amount=54.00)
        self.order_item = OrderItem.objects.create(order=self.order, variant=self.variant, seller=self.seller, unit_price=50.00, quantity=1, total_price=50.00)

    def test_return_request_creation(self):
        ret = ReturnRequest.objects.create(
            order=self.order,
            order_item=self.order_item,
            user=self.user,
            reason='DEFECTIVE_ITEM',
            refund_amount=50.00
        )
        self.assertEqual(ret.status, 'SUBMITTED')
        self.assertEqual(ret.order_item.variant.sku, 'SKU-R')
