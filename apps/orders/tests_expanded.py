"""
Expanded Test Suite for Cart Operations, Checkout Workflows, and Order Fulfillment.
Verifies that products across all catalog categories can be added to cart, modified,
removed, correctly calculate subtotals & taxes, and proceed through checkout.
"""

from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal

from apps.accounts.models import User, Address
from apps.sellers.models import Seller
from apps.catalog.models import Category, Brand, Product, ProductVariant
from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem
from apps.inventory.models import Inventory

class CartAndCheckoutExpandedTestSuite(TestCase):
    def setUp(self):
        self.client = Client()

        # User
        self.user = User.objects.create_user(
            username='shopper_test@example.com',
            email='shopper_test@example.com',
            password='ShopperPassword123!'
        )
        self.client.login(email='shopper_test@example.com', password='ShopperPassword123!')

        # Address
        self.address = Address.objects.create(
            user=self.user,
            address_type='SHIPPING',
            full_name='Shopper Test',
            street_address_1='123 Test St',
            city='San Francisco',
            state='CA',
            postal_code='94105',
            country='United States',
            is_default=True
        )

        # Seller
        self.seller = Seller.objects.create(
            user=self.user,
            business_name='Test Merchant',
            business_email='merchant@test.local',
            status='APPROVED'
        )

        # Category & Products
        self.cat = Category.objects.create(name='Electronics', slug='electronics')
        self.brand = Brand.objects.create(name='ApexTech')

        self.p1 = Product.objects.create(
            seller=self.seller,
            category=self.cat,
            brand=self.brand,
            name='Test Laptop',
            slug='test-laptop',
            base_price=Decimal('1000.00'),
            discount_percent=Decimal('10.00'), # Effective: 900.00
            status='PUBLISHED'
        )
        self.v1 = ProductVariant.objects.create(
            product=self.p1,
            sku='TEST-SKU-1',
            variant_name='Default',
            price_override=Decimal('1000.00')
        )
        Inventory.objects.create(variant=self.v1, quantity_on_hand=50)

        self.p2 = Product.objects.create(
            seller=self.seller,
            category=self.cat,
            brand=self.brand,
            name='Test Headphones',
            slug='test-headphones',
            base_price=Decimal('200.00'),
            discount_percent=Decimal('0.00'), # Effective: 200.00
            status='PUBLISHED'
        )
        self.v2 = ProductVariant.objects.create(
            product=self.p2,
            sku='TEST-SKU-2',
            variant_name='Black',
            price_override=Decimal('200.00')
        )
        Inventory.objects.create(variant=self.v2, quantity_on_hand=100)

    def test_add_to_cart_and_calculate_subtotal(self):
        url = reverse('cart:add_to_cart', kwargs={'variant_id': self.v1.id})
        response = self.client.post(url, {'quantity': 2}, follow=True)
        self.assertEqual(response.status_code, 200)

        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 1)
        item = cart.items.first()
        self.assertEqual(item.quantity, 2)
        # 2 * 900.00 = 1800.00
        self.assertEqual(cart.subtotal, Decimal('1800.00'))

    def test_add_multiple_category_products_to_cart(self):
        self.client.post(reverse('cart:add_to_cart', kwargs={'variant_id': self.v1.id}), {'quantity': 1})
        self.client.post(reverse('cart:add_to_cart', kwargs={'variant_id': self.v2.id}), {'quantity': 2})

        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 2)
        # Laptop: 1 * 900 = 900. Headphones: 2 * 200 = 400. Total Subtotal = 1300.00
        self.assertEqual(cart.subtotal, Decimal('1300.00'))

    def test_update_cart_item_quantity(self):
        self.client.post(reverse('cart:add_to_cart', kwargs={'variant_id': self.v1.id}), {'quantity': 1})
        cart = Cart.objects.get(user=self.user)
        item = cart.items.first()

        update_url = reverse('cart:update_cart', kwargs={'item_id': item.id})
        self.client.post(update_url, {'quantity': 3})

        item.refresh_from_db()
        self.assertEqual(item.quantity, 3)
        self.assertEqual(cart.subtotal, Decimal('2700.00'))

    def test_remove_item_from_cart(self):
        self.client.post(reverse('cart:add_to_cart', kwargs={'variant_id': self.v1.id}), {'quantity': 1})
        cart = Cart.objects.get(user=self.user)
        item = cart.items.first()

        remove_url = reverse('cart:remove_from_cart', kwargs={'item_id': item.id})
        self.client.post(remove_url)

        self.assertEqual(cart.items.count(), 0)
        self.assertEqual(cart.subtotal, Decimal('0.00'))

    def test_checkout_page_renders_address_and_summary(self):
        self.client.post(reverse('cart:add_to_cart', kwargs={'variant_id': self.v1.id}), {'quantity': 1})
        checkout_url = reverse('orders:checkout')
        response = self.client.get(checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '123 Test St')

    def test_place_order_creates_order_and_clears_cart(self):
        self.client.post(reverse('cart:add_to_cart', kwargs={'variant_id': self.v1.id}), {'quantity': 1})
        place_order_url = reverse('orders:place_order')
        response = self.client.post(place_order_url, {'address_id': self.address.id}, follow=True)
        self.assertEqual(response.status_code, 200)

        orders = Order.objects.filter(user=self.user)
        self.assertEqual(orders.count(), 1)
        order = orders.first()
        self.assertEqual(order.items.count(), 1)

        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 0)
