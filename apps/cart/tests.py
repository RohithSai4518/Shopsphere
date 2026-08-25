from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant
from apps.cart.models import CartItem
from apps.cart.context_processors import cart_summary

User = get_user_model()

class CartModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='customer@example.com',
            username='customer@example.com',
            password='CustomerPassword123!'
        )
        self.seller_user = User.objects.create_user(
            email='seller2@example.com',
            username='seller2@example.com',
            password='SellerPassword123!',
            role='SELLER'
        )
        self.seller = Seller.objects.create(user=self.seller_user, business_name='Seller Two', business_email='seller2@example.com')
        self.category = Category.objects.create(name='Gadgets', slug='gadgets')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='Smart Watch',
            slug='smart-watch',
            base_price=200.00,
            discount_percent=0.00
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='SW-01',
            variant_name='Silver'
        )

    def test_cart_item_subtotal(self):
        cart_item = CartItem.objects.create(
            user=self.user,
            variant=self.variant,
            quantity=3
        )
        self.assertEqual(cart_item.subtotal, 600.00)

    def test_cart_summary_uses_decimal_tax_calculation(self):
        CartItem.objects.create(user=self.user, variant=self.variant, quantity=3)
        request = type('Request', (), {'user': self.user})()

        summary = cart_summary(request)

        self.assertEqual(summary['cart_subtotal'], 600.00)
        self.assertEqual(summary['cart_tax'], 49.50)
        self.assertEqual(summary['cart_total'], 649.50)
