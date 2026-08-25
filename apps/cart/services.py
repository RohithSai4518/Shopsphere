from django.db import transaction
from decimal import Decimal
from .models import CartItem, SavedCart, SavedCartItem
from apps.catalog.models import ProductVariant

class CartService:
    @staticmethod
    def add_to_cart(user, variant_id, quantity=1):
        variant = ProductVariant.objects.get(id=variant_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            variant=variant,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    @staticmethod
    def update_cart_item(user, item_id, quantity):
        if quantity <= 0:
            return CartService.remove_cart_item(user, item_id)
        item = CartItem.objects.filter(id=item_id, user=user).first()
        if item:
            item.quantity = quantity
            item.save()
        return item

    @staticmethod
    def remove_cart_item(user, item_id):
        return CartItem.objects.filter(id=item_id, user=user).delete()

    @staticmethod
    @transaction.atomic
    def save_cart_for_later(user, name='Saved Cart'):
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return None

        saved_cart = SavedCart.objects.create(user=user, name=name)
        for item in cart_items:
            SavedCartItem.objects.create(
                saved_cart=saved_cart,
                variant=item.variant,
                quantity=item.quantity
            )

        cart_items.delete()
        return saved_cart

    @staticmethod
    @transaction.atomic
    def restore_saved_cart(user, saved_cart_id):
        saved_cart = SavedCart.objects.filter(id=saved_cart_id, user=user).first()
        if not saved_cart:
            return False

        for item in saved_cart.items.all():
            CartService.add_to_cart(user, item.variant.id, item.quantity)

        saved_cart.delete()
        return True

    @staticmethod
    def calculate_cart_summary(user, coupon=None):
        items = CartItem.objects.filter(user=user)
        subtotal = sum(item.subtotal for item in items) if items.exists() else Decimal('0.00')

        discount_amount = Decimal('0.00')
        if coupon:
            discount_amount = coupon.calculate_discount(subtotal)

        taxable_amount = max(Decimal('0.00'), subtotal - discount_amount)
        tax_amount = round(taxable_amount * Decimal('0.0825'), 2)
        total_amount = round(taxable_amount + tax_amount, 2)

        return {
            'items': items,
            'item_count': sum(i.quantity for i in items),
            'subtotal': subtotal,
            'discount_amount': discount_amount,
            'tax_amount': tax_amount,
            'shipping_amount': Decimal('0.00'),
            'total_amount': total_amount
        }
