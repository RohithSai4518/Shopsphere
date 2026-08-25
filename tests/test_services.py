from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model
from apps.sellers.models import Seller
from apps.catalog.models import Category, Product, ProductVariant
from apps.cart.models import CartItem
from apps.inventory.models import Inventory
from apps.promotions.models import Coupon
from apps.orders.services import OrderService, OrderProcessingError
from apps.inventory.services import InventoryService
from apps.sellers.services import SellerAnalyticsService
from apps.promotions.services import PromotionService, CouponValidationError

User = get_user_model()

class DomainServicesTestCase(TestCase):
    def setUp(self):
        self.customer = User.objects.create_user(
            email='cust_service@example.com',
            username='cust_service@example.com',
            password='CustomerPassword123!'
        )
        self.seller_user = User.objects.create_user(
            email='merchant_service@example.com',
            username='merchant_service@example.com',
            password='MerchantPassword123!',
            role='SELLER'
        )
        self.seller = Seller.objects.create(
            user=self.seller_user,
            business_name='Apex Hardware Direct',
            business_email='merchant_service@example.com',
            commission_rate=10.00
        )
        self.category = Category.objects.create(name='Laptops', slug='laptops')
        self.product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name='ProBook X1',
            slug='probook-x1',
            base_price=1000.00
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            sku='PB-X1-16GB',
            variant_name='16GB RAM'
        )
        self.inventory = Inventory.objects.create(
            variant=self.variant,
            quantity_on_hand=50,
            quantity_reserved=0
        )

    def test_order_service_checkout_flow(self):
        cart_item = CartItem.objects.create(
            user=self.customer,
            variant=self.variant,
            quantity=2
        )
        cart_items = CartItem.objects.filter(user=self.customer)

        order = OrderService.process_checkout(
            user=self.customer,
            cart_items=cart_items,
            shipping_address='100 Test St, San Francisco, CA'
        )

        self.assertEqual(order.subtotal, 2000.00)
        self.assertEqual(order.status, 'CONFIRMED')
        self.assertEqual(order.items.count(), 1)
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity_reserved, 2)

    def test_inventory_service_restock(self):
        InventoryService.restock_variant(self.variant, quantity=25, notes='Unit test restock')
        self.inventory.refresh_from_db()
        self.assertEqual(self.inventory.quantity_on_hand, 75)

    def test_promotion_service_coupon_application(self):
        now = timezone.now()
        coupon = Coupon.objects.create(
            code='SAVE20',
            discount_type='PERCENTAGE',
            discount_value=20.00,
            min_order_subtotal=100.00,
            starts_at=now - timedelta(days=1),
            expires_at=now + timedelta(days=10)
        )

        cpn, discount = PromotionService.validate_and_apply_coupon('SAVE20', 500.00)
        self.assertEqual(cpn.code, 'SAVE20')
        self.assertEqual(discount, 100.00)

    def test_seller_analytics_service(self):
        metrics = SellerAnalyticsService.calculate_seller_metrics(self.seller)
        self.assertEqual(metrics['commission_rate'], 10.00)
