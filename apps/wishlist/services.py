from decimal import Decimal
from .models import Wishlist, WishlistItem, PriceAlert, BackInStockAlert
from apps.catalog.models import Product, ProductVariant
from apps.notifications.services import NotificationService

class WishlistService:
    @staticmethod
    def add_to_wishlist(user, product_id, wishlist_name='My Wishlist'):
        product = Product.objects.get(id=product_id)
        wishlist, _ = Wishlist.objects.get_or_create(user=user, name=wishlist_name)
        item, _ = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        return item

    @staticmethod
    def set_price_alert(user, product_id, target_price):
        product = Product.objects.get(id=product_id)
        alert, _ = PriceAlert.objects.update_or_create(
            user=user,
            product=product,
            defaults={'target_price': Decimal(str(target_price)), 'is_triggered': False}
        )
        return alert

    @staticmethod
    def check_price_alerts_for_product(product):
        effective = Decimal(str(product.effective_price))
        alerts = PriceAlert.objects.filter(product=product, is_triggered=False, target_price__gte=effective)

        for alert in alerts:
            alert.is_triggered = True
            alert.save()

            NotificationService.send_notification(
                user=alert.user,
                title=f"Price Drop Alert: {product.name}",
                message=f"Good news! '{product.name}' has dropped in price to ${effective} (your target was ${alert.target_price}).",
                notification_type='PRICE_DROP',
                action_url=f"/product/{product.slug}/"
            )

    @staticmethod
    def set_back_in_stock_alert(user, variant_id):
        variant = ProductVariant.objects.get(id=variant_id)
        alert, _ = BackInStockAlert.objects.get_or_create(
            user=user,
            variant=variant,
            defaults={'is_notified': False}
        )
        return alert
