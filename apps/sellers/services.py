from django.db import transaction
from django.db.models import Sum, Avg
from decimal import Decimal
from django.utils import timezone
from .models import Seller, SellerSettlement, SellerOnboarding
from apps.orders.models import OrderItem
from apps.reviews.models import Review
from apps.audit.models import SecurityAuditLog

class SellerService:
    @staticmethod
    @transaction.atomic
    def register_seller(user, business_name, business_email, business_phone=None, tax_id=None):
        seller, created = Seller.objects.get_or_create(
            user=user,
            defaults={
                'business_name': business_name,
                'business_email': business_email,
                'business_phone': business_phone,
                'tax_id': tax_id,
                'status': 'PENDING'
            }
        )
        user.role = 'SELLER'
        user.save()

        SellerOnboarding.objects.get_or_create(seller=seller)

        SecurityAuditLog.objects.create(
            user=user,
            action='SELLER_REGISTRATION',
            module='sellers',
            entity_type='Seller',
            entity_id=seller.id
        )

        return seller

    @staticmethod
    def approve_seller(seller, approved_by):
        seller.status = 'APPROVED'
        seller.save()

        onboarding = getattr(seller, 'onboarding', None)
        if onboarding:
            onboarding.is_identity_verified = True
            onboarding.is_tax_verified = True
            onboarding.current_step = 4
            onboarding.save()

        SecurityAuditLog.objects.create(
            user=approved_by,
            action='SELLER_APPROVED',
            module='sellers',
            entity_type='Seller',
            entity_id=seller.id
        )
        return seller

    @staticmethod
    @transaction.atomic
    def generate_settlement(seller, period_start, period_end):
        items = OrderItem.objects.filter(
            seller=seller,
            created_at__gte=period_start,
            created_at__lte=period_end,
            item_status__in=['SHIPPED', 'DELIVERED']
        )
        gross_sales = items.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
        commission_rate = Decimal(str(seller.commission_rate))
        commission_fee = round((gross_sales * commission_rate) / Decimal('100.00'), 2)
        net_payout = round(gross_sales - commission_fee, 2)

        settlement = SellerSettlement.objects.create(
            seller=seller,
            period_start=period_start,
            period_end=period_end,
            gross_sales=gross_sales,
            commission_fee=commission_fee,
            net_payout=net_payout,
            status='PENDING'
        )

        return settlement


class SellerAnalyticsService:
    @staticmethod
    def calculate_seller_metrics(seller):
        items = OrderItem.objects.filter(seller=seller)
        total_revenue = items.aggregate(total=Sum('total_price'))['total'] or Decimal('0.00')
        total_units_sold = items.aggregate(total=Sum('quantity'))['total'] or 0

        commission_rate = Decimal(str(seller.commission_rate))
        commission_paid = round((total_revenue * commission_rate) / Decimal('100.00'), 2)
        net_payout = round(total_revenue - commission_paid, 2)

        avg_rating = Review.objects.filter(product__seller=seller, status='APPROVED').aggregate(avg=Avg('rating'))['avg']
        if avg_rating:
            seller.rating_avg = round(Decimal(str(avg_rating)), 2)
            seller.save()

        return {
            'total_revenue': total_revenue,
            'total_units_sold': total_units_sold,
            'commission_rate': commission_rate,
            'commission_paid': commission_paid,
            'net_payout': net_payout,
            'rating_avg': seller.rating_avg
        }
