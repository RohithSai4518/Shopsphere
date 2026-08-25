from decimal import Decimal
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from .models import RecentlyViewed, SearchHistory, ProductAnalytics, PlatformDailyMetric
from apps.orders.models import Order, OrderItem
from apps.accounts.models import User
from apps.sellers.models import Seller

class AnalyticsService:
    @staticmethod
    def record_product_view(user, product):
        if user and user.is_authenticated:
            RecentlyViewed.objects.update_or_create(
                user=user,
                product=product
            )

        pa, _ = ProductAnalytics.objects.get_or_create(product=product)
        pa.total_views += 1
        pa.save()

    @staticmethod
    def record_cart_addition(product):
        pa, _ = ProductAnalytics.objects.get_or_create(product=product)
        pa.total_cart_additions += 1
        pa.save()

    @staticmethod
    def record_search_query(user, query_text, count):
        if query_text:
            SearchHistory.objects.create(
                user=user if user and user.is_authenticated else None,
                query_text=query_text,
                result_count=count
            )

    @staticmethod
    def calculate_platform_daily_metrics(metric_date=None):
        if not metric_date:
            metric_date = timezone.now().date()

        orders_today = Order.objects.filter(created_at__date=metric_date, status__in=['CONFIRMED', 'SHIPPED', 'DELIVERED'])
        gmv = orders_today.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        order_count = orders_today.count()

        active_customers = User.objects.filter(role='CUSTOMER', is_active=True).count()
        active_sellers = Seller.objects.filter(status='APPROVED').count()

        metric, _ = PlatformDailyMetric.objects.update_or_create(
            metric_date=metric_date,
            defaults={
                'gross_merchandise_value': gmv,
                'order_count': order_count,
                'active_customers': active_customers,
                'active_sellers': active_sellers
            }
        )
        return metric
