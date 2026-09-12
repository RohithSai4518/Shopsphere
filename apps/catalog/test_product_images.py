import os
from decimal import Decimal
from django.test import TestCase, Client
from django.conf import settings
from django.core.management import call_command
from django.urls import reverse

from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.catalog.models import Category, Brand, Product, ProductImage
from data.catalog_expanded_dataset import RAW_PRODUCT_CATALOG


class ProductImageMatchingTests(TestCase):
    """
    Tests ensuring all products accurately match their photographic image assets
    in media/products/<slug>.jpg with zero broken or generic external fallbacks.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='seller_img_test@example.com',
            email='seller_img_test@example.com',
            password='TestPassword123!',
            role='SELLER'
        )
        self.seller = Seller.objects.create(
            user=self.user,
            business_name='Apex Electronics Testing',
            business_email='seller_img_test@example.com',
            status='APPROVED'
        )
        self.category = Category.objects.create(
            name='Electronics & Gadgets',
            slug='electronics',
            is_active=True
        )
        self.brand = Brand.objects.create(
            name='Spectra Optics',
            description='Professional optics and lenses'
        )

    def test_all_80_catalog_dataset_images_exist_on_disk(self):
        """Verify that every single product in RAW_PRODUCT_CATALOG has a valid local image file."""
        self.assertEqual(len(RAW_PRODUCT_CATALOG), 80, "Expected exactly 80 products in RAW_PRODUCT_CATALOG")

        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        self.assertTrue(os.path.exists(media_products_dir), "media/products directory must exist")

        missing_files = []
        undersized_files = []

        for pdata in RAW_PRODUCT_CATALOG:
            slug = pdata['slug']
            image_url = pdata.get('image_url', '')

            self.assertTrue(
                image_url.startswith('/media/products/'),
                f"Product '{slug}' image_url '{image_url}' should start with /media/products/"
            )

            expected_filename = f"{slug}.jpg"
            disk_path = os.path.join(media_products_dir, expected_filename)

            if not os.path.exists(disk_path):
                missing_files.append(expected_filename)
            else:
                size = os.path.getsize(disk_path)
                if size < 1024:  # Less than 1 KB
                    undersized_files.append((expected_filename, size))

        self.assertEqual(missing_files, [], f"Missing image files on disk: {missing_files}")
        self.assertEqual(undersized_files, [], f"Undersized or empty image files: {undersized_files}")

    def test_product_primary_image_resolution_and_fallback(self):
        """Test Product.primary_image returns DB image when present and falls back to local media path."""
        product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            brand=self.brand,
            name='QuantumX 4K Ultra HD Smart Home Cinema Projector',
            slug='quantumx-4k-smart-projector',
            base_price=Decimal('499.99'),
            status='PUBLISHED'
        )

        # 1. Fallback when no ProductImage object exists in DB
        self.assertEqual(product.primary_image, '/media/products/quantumx-4k-smart-projector.jpg')

        # 2. When ProductImage object exists in DB
        ProductImage.objects.create(
            product=product,
            image_url='/media/products/quantumx-4k-smart-projector.jpg',
            is_primary=True,
            display_order=1
        )
        self.assertEqual(product.primary_image, '/media/products/quantumx-4k-smart-projector.jpg')

    def test_sync_product_images_command(self):
        """Test the sync_product_images management command updates stale image records."""
        product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            brand=self.brand,
            name='AeroTech Pro 4K Dual-Camera GPS Drone',
            slug='aerotech-drone-pro-4k',
            base_price=Decimal('649.99'),
            status='PUBLISHED'
        )
        # Create a stale Unsplash image
        img = ProductImage.objects.create(
            product=product,
            image_url='https://images.unsplash.com/photo-stale-placeholder',
            is_primary=True,
            display_order=1
        )

        # Run command
        call_command('sync_product_images')

        img.refresh_from_db()
        self.assertEqual(img.image_url, '/media/products/aerotech-drone-pro-4k.jpg')
        self.assertTrue(img.is_primary)

    def test_catalog_views_render_matched_image(self):
        """Verify that catalog list and product detail views output the matched image URL."""
        product = Product.objects.create(
            seller=self.seller,
            category=self.category,
            brand=self.brand,
            name='ApexPro X15 Ultra Laptop',
            slug='apexpro-x15-ultra-laptop',
            base_price=Decimal('1499.99'),
            status='PUBLISHED'
        )
        ProductImage.objects.create(
            product=product,
            image_url='/media/products/apexpro-x15-ultra-laptop.jpg',
            is_primary=True,
            display_order=1
        )

        # Product detail page
        detail_res = self.client.get(reverse('catalog:product_detail', kwargs={'slug': product.slug}))
        self.assertEqual(detail_res.status_code, 200)
        self.assertContains(detail_res, '/media/products/apexpro-x15-ultra-laptop.jpg')
