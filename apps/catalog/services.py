from django.db.models import Q, Avg, Count
from decimal import Decimal
from .models import Product, Category, ProductVariant, Brand, ProductBundle, ProductRelationship, ProductQuestion, ProductAnswer, ProductModerationLog, Tag
from apps.audit.models import SecurityAuditLog

class CatalogService:
    @staticmethod
    def search_products(query='', category_slug=None, brand_id=None, tag_slug=None, min_price=None, max_price=None, min_rating=None, in_stock_only=False, is_featured=None, sort_by='newest'):
        products = Product.objects.filter(status='PUBLISHED').select_related('seller', 'category', 'brand').prefetch_related('images', 'variants', 'reviews', 'tags')

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(brand_name__icontains=query) |
                Q(category__name__icontains=query)
            )

        if category_slug:
            # Recursive category hierarchy match
            category = Category.objects.filter(slug=category_slug).first()
            if category:
                child_ids = list(category.children.values_list('id', flat=True))
                child_ids.append(category.id)
                products = products.filter(category_id__in=child_ids)

        if brand_id:
            products = products.filter(brand_id=brand_id)

        if tag_slug:
            products = products.filter(tags__slug=tag_slug)

        if min_price not in (None, ''):
            products = products.filter(base_price__gte=Decimal(str(min_price)))

        if max_price not in (None, ''):
            products = products.filter(base_price__lte=Decimal(str(max_price)))

        if is_featured:
            products = products.filter(is_featured=True)

        if in_stock_only:
            products = products.filter(variants__inventory__quantity_on_hand__gt=0).distinct()

        if min_rating is not None:
            products = products.annotate(avg_rating=Avg('reviews__rating')).filter(avg_rating__gte=float(min_rating))

        # Sorting
        if sort_by == 'price_asc':
            products = products.order_by('base_price')
        elif sort_by == 'price_desc':
            products = products.order_by('-base_price')
        elif sort_by == 'popular':
            products = products.order_by('-is_bestseller', '-created_at')
        elif sort_by == 'rating':
            products = products.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        else:
            products = products.order_by('-created_at')

        return products

    @staticmethod
    def get_search_suggestions(query, limit=5):
        if not query or len(query) < 2:
            return []
        products = Product.objects.filter(status='PUBLISHED', name__icontains=query).values('name', 'slug', 'base_price')[:limit]
        return list(products)

    @staticmethod
    def get_recommendations_for_product(product, limit=4):
        # 1. Frequently Bought Together or Related
        relationships = ProductRelationship.objects.filter(source_product=product).select_related('target_product')
        rel_products = [rel.target_product for rel in relationships if rel.target_product.status == 'PUBLISHED']

        if len(rel_products) < limit:
            # 2. Fill with same category products
            same_cat = Product.objects.filter(category=product.category, status='PUBLISHED').exclude(id=product.id)[:limit - len(rel_products)]
            rel_products.extend(list(same_cat))

        return rel_products[:limit]

    @staticmethod
    def get_bundle_savings(bundle):
        total_individual_price = sum(Decimal(str(item.product.effective_price)) for item in bundle.items.all())
        discount_pct = Decimal(str(bundle.discount_percentage))
        discount_val = (total_individual_price * discount_pct) / Decimal('100.00')
        bundle_price = round(total_individual_price - discount_val, 2)
        return {
            'original_total': total_individual_price,
            'bundle_price': bundle_price,
            'savings': round(discount_val, 2)
        }

    @staticmethod
    def moderate_product(product, new_status, moderator=None, reason=None):
        old_status = product.status
        product.status = new_status
        product.save()

        ProductModerationLog.objects.create(
            product=product,
            moderator=moderator,
            status_from=old_status,
            status_to=new_status,
            reason=reason
        )

        if moderator:
            SecurityAuditLog.objects.create(
                user=moderator,
                action='PRODUCT_MODERATION',
                module='catalog',
                entity_type='Product',
                entity_id=product.id,
                metadata_json=f'{{"from": "{old_status}", "to": "{new_status}"}}'
            )

        return product
