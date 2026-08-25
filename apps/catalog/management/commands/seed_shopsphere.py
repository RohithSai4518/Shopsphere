from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from apps.accounts.models import User, Address, UserPreference
from apps.rbac.models import Role, Permission, RolePermission
from apps.sellers.models import Seller
from apps.catalog.models import Category, Brand, Product, ProductVariant, ProductSpecification, ProductImage, ProductBundle, BundleItem
from apps.inventory.models import WarehouseLocation, Inventory, InventoryTransaction
from apps.promotions.models import Coupon, PromotionalCampaign
from apps.reviews.models import Review, ReviewVote
from apps.support.models import SupportTicket, SupportMessage
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment

class Command(BaseCommand):
    help = 'Seeds ShopSphere Python Marketplace with complete realistic synthetic data across 36 relational entities.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding ShopSphere Python Full-Stack Marketplace Database...'))

        # 1. RBAC Roles & Permissions
        role_admin, _ = Role.objects.get_or_create(name='ADMIN', defaults={'description': 'Platform Administrator'})
        role_seller, _ = Role.objects.get_or_create(name='SELLER', defaults={'description': 'Verified Merchant Seller'})
        role_customer, _ = Role.objects.get_or_create(name='CUSTOMER', defaults={'description': 'Platform Customer'})
        role_support, _ = Role.objects.get_or_create(name='SUPPORT', defaults={'description': 'Customer Support Staff'})

        perm_cat, _ = Permission.objects.get_or_create(code='manage_catalog', defaults={'module': 'catalog', 'description': 'Manage Catalog Products'})
        perm_orders, _ = Permission.objects.get_or_create(code='manage_orders', defaults={'module': 'orders', 'description': 'Fulfill Orders'})
        RolePermission.objects.get_or_create(role=role_seller, permission=perm_cat)
        RolePermission.objects.get_or_create(role=role_seller, permission=perm_orders)

        # 2. Users
        admin_user, _ = User.objects.get_or_create(
            email='admin@shopsphere.local',
            defaults={
                'username': 'admin@shopsphere.local',
                'first_name': 'Platform',
                'last_name': 'Administrator',
                'role': 'ADMIN',
                'is_staff': True,
                'is_superuser': True
            }
        )
        admin_user.set_password('AdminPass123!')
        admin_user.save()
        UserPreference.objects.get_or_create(user=admin_user)

        seller_user, _ = User.objects.get_or_create(
            email='merchant@apextech.com',
            defaults={
                'username': 'merchant@apextech.com',
                'first_name': 'Apex',
                'last_name': 'Merchant',
                'role': 'SELLER'
            }
        )
        seller_user.set_password('SellerPass123!')
        seller_user.save()
        UserPreference.objects.get_or_create(user=seller_user)

        customer_user, _ = User.objects.get_or_create(
            email='jane.customer@example.com',
            defaults={
                'username': 'jane.customer@example.com',
                'first_name': 'Jane',
                'last_name': 'Shopper',
                'role': 'CUSTOMER'
            }
        )
        customer_user.set_password('CustomerPass123!')
        customer_user.save()
        UserPreference.objects.get_or_create(user=customer_user)

        # 3. Seller Profile
        seller_profile, _ = Seller.objects.get_or_create(
            user=seller_user,
            defaults={
                'business_name': 'Apex Electronics Merchant Store',
                'business_email': 'merchant@apextech.com',
                'business_phone': '+15551234567',
                'tax_id': 'TAX-9988-APEX',
                'commission_rate': 8.50,
                'rating_avg': 4.85,
                'status': 'APPROVED'
            }
        )

        # 4. Address Book
        Address.objects.get_or_create(
            user=customer_user,
            is_default=True,
            defaults={
                'address_type': 'SHIPPING',
                'full_name': 'Jane Shopper',
                'street_address_1': '100 Synthetic Way',
                'city': 'San Francisco',
                'state': 'CA',
                'postal_code': '94105',
                'country': 'United States'
            }
        )

        # 5. Categories & Brands
        cat_electronics, _ = Category.objects.get_or_create(
            slug='electronics',
            defaults={'name': 'Electronics', 'description': 'Laptops, Smartphones, Audio, and Gadgets', 'icon_url': 'laptop'}
        )
        cat_laptops, _ = Category.objects.get_or_create(
            slug='laptops',
            defaults={'parent': cat_electronics, 'name': 'Laptops & Computers', 'description': 'High performance workstation laptops'}
        )
        cat_audio, _ = Category.objects.get_or_create(
            slug='audio-headphones',
            defaults={'parent': cat_electronics, 'name': 'Audio & Headphones', 'description': 'Noise cancelling headphones and soundbars'}
        )

        brand_apex, _ = Brand.objects.get_or_create(name='ApexTech', defaults={'description': 'Premium Workstation Hardware'})
        brand_sound, _ = Brand.objects.get_or_create(name='SoundWave', defaults={'description': 'Studio Quality Audio Equipment'})

        # 6. Products, Variants, Specifications, Images
        prod_laptop, _ = Product.objects.get_or_create(
            slug='apexpro-x15-ultra-laptop',
            defaults={
                'seller': seller_profile,
                'category': cat_laptops,
                'brand': brand_apex,
                'name': 'ApexPro X15 Ultra Laptop',
                'brand_name': 'ApexTech',
                'description': 'The ApexPro X15 features an 8-core CPU, 32GB RAM, 1TB NVMe SSD, and 15.6-inch 4K OLED display.',
                'base_price': 1499.99,
                'discount_percent': 10.00,
                'tax_rate': 8.25,
                'status': 'PUBLISHED'
            }
        )

        var_laptop1, _ = ProductVariant.objects.get_or_create(
            product=prod_laptop,
            sku='APX-X15-32GB',
            defaults={'variant_name': '32GB RAM / 1TB SSD', 'price_override': 1499.99}
        )

        ProductSpecification.objects.get_or_create(product=prod_laptop, spec_key='Processor', defaults={'spec_value': '8-Core Ultra Chip', 'display_group': 'Performance'})
        ProductSpecification.objects.get_or_create(product=prod_laptop, spec_key='Display', defaults={'spec_value': '15.6-inch 4K OLED HDR', 'display_group': 'Display'})

        ProductImage.objects.get_or_create(
            product=prod_laptop,
            image_url='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80',
            defaults={'is_primary': True}
        )

        prod_earbuds, _ = Product.objects.get_or_create(
            slug='soundwave-pro-wireless-earbuds',
            defaults={
                'seller': seller_profile,
                'category': cat_audio,
                'brand': brand_sound,
                'name': 'SoundWave Pro ANC Wireless Earbuds',
                'brand_name': 'SoundWave',
                'description': 'Studio quality active noise-cancelling earbuds with 36-hour battery life and wireless charging case.',
                'base_price': 199.99,
                'discount_percent': 15.00,
                'tax_rate': 8.25,
                'status': 'PUBLISHED'
            }
        )

        var_earbuds1, _ = ProductVariant.objects.get_or_create(
            product=prod_earbuds,
            sku='SW-ANC-BLK',
            defaults={'variant_name': 'Matte Black', 'price_override': 199.99}
        )

        ProductImage.objects.get_or_create(
            product=prod_earbuds,
            image_url='https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=800&q=80',
            defaults={'is_primary': True}
        )

        additional_categories = [
            ('smartphones', 'Smartphones & Tablets', 'Mobile devices, tablets, and accessories'),
            ('cameras', 'Cameras & Photography', 'Cameras, lenses, and photography gear'),
            ('home-kitchen', 'Home & Kitchen', 'Appliances, cookware, and home essentials'),
            ('fashion', 'Fashion', 'Clothing, shoes, and everyday accessories'),
            ('beauty', 'Beauty & Personal Care', 'Skincare, grooming, and wellness products'),
            ('sports', 'Sports & Outdoors', 'Fitness equipment and outdoor gear'),
            ('books', 'Books & Media', 'Books, games, and entertainment'),
            ('office', 'Office Supplies', 'Workplace essentials and productivity tools'),
        ]
        seeded_categories = {
            slug: Category.objects.get_or_create(
                slug=slug,
                defaults={'name': name, 'description': description, 'icon_url': slug}
            )[0]
            for slug, name, description in additional_categories
        }

        additional_products = [
            ('nova-phone-z1', 'Nova Phone Z1', 'smartphones', 'A modern 5G smartphone with a bright OLED display and all-day battery.', 699.99, 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=800&q=80'),
            ('nova-tablet-air', 'Nova Tablet Air 11', 'smartphones', 'A lightweight tablet for streaming, reading, and creative work.', 429.99, 'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=800&q=80'),
            ('spectra-mirrorless-m1', 'Spectra Mirrorless M1 Camera', 'cameras', 'A compact mirrorless camera with fast autofocus for travel photography.', 899.99, 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=800&q=80'),
            ('homebrew-coffee-maker', 'HomeBrew Smart Coffee Maker', 'home-kitchen', 'Programmable coffee maker with app scheduling and thermal carafe.', 129.99, 'https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?auto=format&fit=crop&w=800&q=80'),
            ('chefline-cookware-set', 'ChefLine 10-Piece Cookware Set', 'home-kitchen', 'Durable non-stick cookware set for everyday meals.', 159.99, 'https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=800&q=80'),
            ('northstar-running-shoes', 'NorthStar Trail Running Shoes', 'fashion', 'Cushioned running shoes with a breathable upper and grippy outsole.', 89.99, 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=800&q=80'),
            ('luma-skin-care-kit', 'Luma Daily Skin Care Kit', 'beauty', 'A simple daily cleanser, moisturizer, and SPF routine.', 54.99, 'https://images.unsplash.com/photo-1556229010-6c3f2c9ca5f8?auto=format&fit=crop&w=800&q=80'),
            ('peak-yoga-mat', 'Peak Performance Yoga Mat', 'sports', 'Non-slip exercise mat with extra cushioning for home workouts.', 39.99, 'https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?auto=format&fit=crop&w=800&q=80'),
            ('trailblazer-daypack', 'TrailBlazer Outdoor Daypack', 'sports', 'Weather-resistant daypack with hydration and laptop compartments.', 74.99, 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80'),
            ('atlas-cookbook', 'Atlas Weeknight Cookbook', 'books', 'Practical recipes for quick and flavorful home-cooked dinners.', 24.99, 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&w=800&q=80'),
            ('papertrail-notebook-set', 'PaperTrail Premium Notebook Set', 'office', 'Three hardcover notebooks for planning, notes, and sketches.', 19.99, 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?auto=format&fit=crop&w=800&q=80'),
            ('focusdesk-lamp', 'FocusDesk LED Task Lamp', 'office', 'Adjustable LED desk lamp with USB charging and warm-to-cool light.', 44.99, 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80'),
        ]
        for slug, name, category_slug, description, price, image_url in additional_products:
            product, _ = Product.objects.get_or_create(
                slug=slug,
                defaults={
                    'seller': seller_profile,
                    'category': seeded_categories[category_slug],
                    'brand': brand_apex,
                    'name': name,
                    'brand_name': 'ApexTech',
                    'description': description,
                    'base_price': price,
                    'tax_rate': 8.25,
                    'status': 'PUBLISHED'
                }
            )
            ProductVariant.objects.get_or_create(
                product=product,
                sku=f'{slug.upper().replace("-", "-")}-STD',
                defaults={'variant_name': 'Standard Edition', 'price_override': price}
            )
            ProductImage.objects.get_or_create(
                product=product,
                image_url=image_url,
                defaults={'is_primary': True}
            )

        # Ensure every active category has a complete, browseable product range.
        product_templates = [
            ('Essential', 'A dependable everyday choice'),
            ('Select', 'A thoughtfully designed customer favorite'),
            ('Pro', 'A performance-focused option for demanding use'),
            ('Elite', 'A premium option with upgraded features'),
            ('Compact', 'A space-saving option for flexible setups'),
            ('Classic', 'A timeless option built for daily use'),
            ('Plus', 'A versatile option with added convenience'),
            ('Advanced', 'A modern option with enhanced capability'),
            ('Signature', 'A refined option for discerning customers'),
            ('Max', 'A feature-rich option for the complete experience'),
        ]
        category_product_counts = {}
        products_created = 0
        for category in Category.objects.filter(is_active=True).order_by('slug'):
            existing_count = category.products.count()
            for product_number in range(existing_count + 1, 11):
                template_name, template_description = product_templates[product_number - 1]
                product_slug = f'{category.slug}-{template_name.lower()}-{product_number}'
                product, created = Product.objects.get_or_create(
                    slug=product_slug,
                    defaults={
                        'seller': seller_profile,
                        'category': category,
                        'brand': brand_apex,
                        'name': f'{category.name} {template_name} {product_number}',
                        'brand_name': 'ApexTech',
                        'description': f'{template_description} for {category.name.lower()}.',
                        'base_price': Decimal('24.99') + (Decimal(product_number) * Decimal('17.50')),
                        'tax_rate': Decimal('8.25'),
                        'status': 'PUBLISHED'
                    }
                )
                variant, _ = ProductVariant.objects.get_or_create(
                    product=product,
                    sku=f'{category.slug.upper().replace("-", "_")}-{product_number:02d}-STD',
                    defaults={'variant_name': 'Standard Edition', 'price_override': product.base_price}
                )
                ProductImage.objects.get_or_create(
                    product=product,
                    image_url='https://images.unsplash.com/photo-1526738549149-8e07eca6c147?auto=format&fit=crop&w=800&q=80',
                    defaults={'is_primary': True}
                )
                Inventory.objects.get_or_create(
                    variant=variant,
                    defaults={'quantity_on_hand': 50, 'reorder_threshold': 5}
                )
                if created:
                    products_created += 1

            category_product_counts[category.slug] = category.products.count()

        self.stdout.write(self.style.SUCCESS(
            f'Product catalog normalized: {products_created} products added; '
            f'{len(category_product_counts)} active categories now have at least 10 products.'
        ))

        # 7. Warehouse & Inventory Ledger
        warehouse, _ = WarehouseLocation.objects.get_or_create(
            code='WH-WEST-01',
            defaults={'name': 'Pacific Logistics Distribution Center', 'address': '500 Logistics Way', 'city': 'Reno', 'state': 'NV', 'country': 'United States'}
        )

        inv_laptop, _ = Inventory.objects.get_or_create(
            variant=var_laptop1,
            defaults={'quantity_on_hand': 45, 'quantity_reserved': 2, 'reorder_threshold': 5}
        )
        inv_earbuds, _ = Inventory.objects.get_or_create(
            variant=var_earbuds1,
            defaults={'quantity_on_hand': 120, 'quantity_reserved': 5, 'reorder_threshold': 10}
        )

        InventoryTransaction.objects.get_or_create(
            variant=var_laptop1,
            transaction_type='RECEIPT',
            quantity=50,
            defaults={'reference_type': 'RESTOCK', 'reference_id': 'RESTOCK-991', 'notes': 'Initial Warehouse Receipt'}
        )

        # 8. Coupons & Promotions
        now = timezone.now()
        coupon_welcome, _ = Coupon.objects.get_or_create(
            code='WELCOME10',
            defaults={
                'discount_type': 'PERCENTAGE',
                'discount_value': 10.00,
                'min_order_subtotal': 50.00,
                'starts_at': now - timedelta(days=1),
                'expires_at': now + timedelta(days=365)
            }
        )

        # 9. Orders & Fulfillment Items
        order1, _ = Order.objects.get_or_create(
            order_number='ORD-20260101-1001',
            defaults={
                'user': customer_user,
                'status': 'CONFIRMED',
                'subtotal': 1349.99,
                'tax_amount': 111.37,
                'shipping_amount': 0.00,
                'discount_amount': 135.00,
                'total_amount': 1326.36,
                'shipping_address_json': '100 Synthetic Way, San Francisco, CA 94105'
            }
        )

        order_item1, _ = OrderItem.objects.get_or_create(
            order=order1,
            variant=var_laptop1,
            defaults={
                'seller': seller_profile,
                'unit_price': 1349.99,
                'discount_amount': 135.00,
                'tax_amount': 111.37,
                'quantity': 1,
                'total_price': 1349.99,
                'item_status': 'PENDING'
            }
        )

        Payment.objects.get_or_create(
            order=order1,
            transaction_reference='TXN-9988776655',
            defaults={'amount': 1326.36, 'status': 'SUCCESS', 'payment_method': 'CREDIT_CARD_SANDBOX'}
        )

        # 10. Reviews & Support Tickets
        Review.objects.get_or_create(
            product=prod_laptop,
            user=customer_user,
            defaults={
                'rating': 5,
                'title': 'Outstanding Performance!',
                'comment': 'The ApexPro X15 handles heavy software development flawlessly.',
                'is_verified_purchase': True,
                'status': 'APPROVED',
                'helpful_votes': 12
            }
        )

        ticket, _ = SupportTicket.objects.get_or_create(
            ticket_number='TKT-10042',
            defaults={
                'user': customer_user,
                'order': order1,
                'subject': 'Order Tracking Inquiry',
                'category': 'ORDER_ISSUE',
                'priority': 'HIGH',
                'status': 'OPEN'
            }
        )

        SupportMessage.objects.get_or_create(
            ticket=ticket,
            sender=customer_user,
            defaults={'message': 'Hello, when will my ApexPro X15 laptop ship?'}
        )

        self.stdout.write(self.style.SUCCESS('[SUCCESS] ShopSphere Python Full-Stack Seeding Completed Successfully!'))
