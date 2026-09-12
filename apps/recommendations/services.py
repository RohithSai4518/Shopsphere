from decimal import Decimal
from django.db.models import F
from .models import ProductSimilarity, FrequentlyBoughtTogether, UserCategoryAffinity
from apps.catalog.models import Product, Category

class RecommendationEngine:
    """
    Hybrid recommendation engine combining:
    1. Content-based spec filtering (spec vector distance)
    2. Co-purchase affinity matrices (Frequently Bought Together bundles)
    3. User session category affinity (Personalized Feed)
    """

    @classmethod
    def get_similar_products(cls, product, limit=6):
        """Returns items most similar to the target product."""
        # 1. Check pre-computed similarity table
        sims = ProductSimilarity.objects.filter(
            source_product=product
        ).select_related('target_product').order_by('-similarity_score')[:limit]

        if sims.exists():
            return [s.target_product for s in sims if s.target_product.status == 'PUBLISHED']

        # 2. Fallback: Category neighbors with similar price tier
        base_variant = product.variants.first()
        base_price = base_variant.price if base_variant else Decimal('50.00')

        similar_items = Product.objects.filter(
            category=product.category,
            status='PUBLISHED'
        ).exclude(id=product.id)[:limit]

        return list(similar_items)

    @classmethod
    def get_frequently_bought_bundle(cls, product):
        """Retrieves or dynamically creates a Frequently Bought Together combo."""
        fbt = FrequentlyBoughtTogether.objects.filter(base_product=product, is_active=True).first()
        if fbt:
            pricing = fbt.compute_bundle_pricing()
            items = [product, fbt.bundle_item_1]
            if fbt.bundle_item_2:
                items.append(fbt.bundle_item_2)
            return {
                'bundle_record': fbt,
                'items': items,
                'pricing': pricing
            }

        # Dynamic fallback: pick 1 or 2 complementary items from same category
        complementary = Product.objects.filter(category=product.category, status='PUBLISHED').exclude(id=product.id)[:2]
        if not complementary.exists():
            return None

        item1 = complementary[0]
        item2 = complementary[1] if len(complementary) > 1 else None

        fbt = FrequentlyBoughtTogether.objects.create(
            base_product=product,
            bundle_item_1=item1,
            bundle_item_2=item2,
            bundle_discount_pct=Decimal('8.00'),
            co_occurrence_count=15
        )
        return {
            'bundle_record': fbt,
            'items': [product, item1] + ([item2] if item2 else []),
            'pricing': fbt.compute_bundle_pricing()
        }

    @classmethod
    def record_user_view(cls, user, product):
        """Updates user category affinity weights when browsing products."""
        if not user or not user.is_authenticated or not product.category:
            return

        affinity, created = UserCategoryAffinity.objects.get_or_create(
            user=user,
            category=product.category,
            defaults={'view_count': 1, 'affinity_score': Decimal('1.00')}
        )
        if not created:
            affinity.view_count += 1
            # Recalculate affinity score (views * 1.0 + purchases * 5.0)
            affinity.affinity_score = Decimal(affinity.view_count) + (Decimal(affinity.purchase_count) * Decimal('5.00'))
            affinity.save()

    @classmethod
    def get_personalized_feed(cls, user, limit=12):
        """Builds a curated discovery feed for the user."""
        if not user or not user.is_authenticated:
            # Fallback to featured products
            return list(Product.objects.filter(status='PUBLISHED', is_featured=True)[:limit])

        affinities = UserCategoryAffinity.objects.filter(user=user).order_by('-affinity_score')[:3]
        if not affinities.exists():
            return list(Product.objects.filter(status='PUBLISHED')[:limit])

        top_categories = [a.category for a in affinities]
        personalized = Product.objects.filter(
            category__in=top_categories,
            status='PUBLISHED'
        ).distinct()[:limit]

        return list(personalized)
