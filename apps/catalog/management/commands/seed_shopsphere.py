from django.core.management.base import BaseCommand
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
import random
import json

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

from data.catalog_expanded_dataset import EXPANDED_CATEGORIES, EXPANDED_BRANDS, RAW_PRODUCT_CATALOG

class Command(BaseCommand):
    help = 'Seeds ShopSphere Python Marketplace with complete realistic synthetic data across 112 products and 16 categories.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding ShopSphere Marketplace Database...'))

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
        category_map = {}
        for cdata in EXPANDED_CATEGORIES:
            cat_obj, _ = Category.objects.get_or_create(
                slug=cdata['slug'],
                defaults={
                    'name': cdata['name'],
                    'description': cdata['description'],
                    'icon_url': cdata['icon_url'],
                    'display_order': cdata['display_order'],
                    'is_active': True
                }
            )
            # Update fields if existed
            cat_obj.name = cdata['name']
            cat_obj.description = cdata['description']
            cat_obj.icon_url = cdata['icon_url']
            cat_obj.display_order = cdata['display_order']
            cat_obj.is_active = True
            cat_obj.save()
            category_map[cdata['slug']] = cat_obj

        brand_map = {}
        for bdata in EXPANDED_BRANDS:
            bname = bdata['name']
            brand_obj, _ = Brand.objects.get_or_create(
                name=bname,
                defaults={
                    'description': bdata['description'],
                    'website': bdata['website']
                }
            )
            brand_map[bname] = brand_obj

        # Clean up obsolete products that are not part of the defined 112 catalog products
        valid_slugs = {p['slug'] for p in RAW_PRODUCT_CATALOG}
        for obsolete_prod in Product.objects.exclude(slug__in=valid_slugs):
            if not obsolete_prod.variants.filter(order_items__isnull=False).exists():
                obsolete_prod.delete()

        # 6. Seed Expanded Catalog Products
        products_seeded = 0
        variants_seeded = 0
        reviews_seeded = 0

        for pdata in RAW_PRODUCT_CATALOG:
            cat_obj = category_map.get(pdata['category_slug'])
            brand_obj = brand_map.get(pdata['brand_name']) or brand_map.get('ApexTech')

            product, created = Product.objects.get_or_create(
                slug=pdata['slug'],
                defaults={
                    'seller': seller_profile,
                    'category': cat_obj,
                    'brand': brand_obj,
                    'name': pdata['name'],
                    'brand_name': pdata['brand_name'],
                    'description': pdata['description'],
                    'base_price': Decimal(str(pdata['base_price'])),
                    'discount_percent': Decimal(str(pdata['discount_percent'])),
                    'tax_rate': Decimal('8.25'),
                    'status': 'PUBLISHED',
                    'is_featured': pdata.get('is_featured', False),
                    'is_bestseller': pdata.get('is_bestseller', False),
                    'is_trending': pdata.get('is_featured', False) or pdata.get('is_bestseller', False)
                }
            )
            if not created:
                product.seller = seller_profile
                product.category = cat_obj
                product.brand = brand_obj
                product.name = pdata['name']
                product.brand_name = pdata['brand_name']
                product.description = pdata['description']
                product.base_price = Decimal(str(pdata['base_price']))
                product.discount_percent = Decimal(str(pdata['discount_percent']))
                product.status = 'PUBLISHED'
                product.is_featured = pdata.get('is_featured', False)
                product.is_bestseller = pdata.get('is_bestseller', False)
                product.save()

            products_seeded += 1

            # Primary Image
            primary_img = ProductImage.objects.filter(product=product, is_primary=True).first()
            if primary_img:
                if primary_img.image_url != pdata['image_url']:
                    primary_img.image_url = pdata['image_url']
                    primary_img.save()
            else:
                ProductImage.objects.create(
                    product=product,
                    image_url=pdata['image_url'],
                    is_primary=True,
                    display_order=1
                )

            # Variants
            for vdata in pdata.get('variants', []):
                v_sku = vdata['sku']
                variant, v_created = ProductVariant.objects.get_or_create(
                    sku=v_sku,
                    defaults={
                        'product': product,
                        'variant_name': vdata['variant_name'],
                        'price_override': Decimal(str(vdata['price'])),
                        'attributes_json': json.dumps(vdata.get('attrs', {}))
                    }
                )
                if not v_created:
                    variant.product = product
                    variant.variant_name = vdata['variant_name']
                    variant.price_override = Decimal(str(vdata['price']))
                    variant.attributes_json = json.dumps(vdata.get('attrs', {}))
                    variant.save()
                variants_seeded += 1

                # Inventory
                Inventory.objects.get_or_create(
                    variant=variant,
                    defaults={'quantity_on_hand': 100, 'quantity_reserved': 2, 'reorder_threshold': 10}
                )

            # Specifications
            for spec_tuple in pdata.get('specs', []):
                s_key, s_val, s_grp = spec_tuple
                ProductSpecification.objects.get_or_create(
                    product=product,
                    spec_key=s_key,
                    defaults={'spec_value': s_val, 'display_group': s_grp}
                )

            # Seed Reviews for realistic ratings (4.5+ average)
            if not Review.objects.filter(product=product).exists():
                Review.objects.create(
                    product=product,
                    user=customer_user,
                    rating=5 if pdata.get('is_bestseller') else 4,
                    title=f"Great product: {product.name}",
                    comment=f"I have been using {product.name} daily. Superior quality, matches description exactly.",
                    is_verified_purchase=True,
                    status='APPROVED',
                    helpful_votes=random.randint(5, 25)
                )
                reviews_seeded += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeded {products_seeded} products, {variants_seeded} variants across {len(category_map)} active categories.'
        ))

        # 7. Warehouse & Inventory Ledger
        warehouse, _ = WarehouseLocation.objects.get_or_create(
            code='WH-WEST-01',
            defaults={'name': 'Pacific Logistics Distribution Center', 'address': '500 Logistics Way', 'city': 'Reno', 'state': 'NV', 'country': 'United States'}
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
        first_product = Product.objects.filter(slug='apexpro-x15-ultra-laptop').first() or Product.objects.first()
        first_variant = first_product.variants.first()

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

        if first_variant:
            OrderItem.objects.get_or_create(
                order=order1,
                variant=first_variant,
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

        # 10. Support Ticket
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
            defaults={'message': 'Hello, when will my order ship?'}
        )

        self.stdout.write(self.style.SUCCESS('[SUCCESS] ShopSphere Seeding Completed Successfully!'))
