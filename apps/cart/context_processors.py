from .models import CartItem
from decimal import Decimal

def cart_summary(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
        total_count = sum(item.quantity for item in items)
        subtotal = sum(item.subtotal for item in items)
        tax_estimate = round(subtotal * Decimal('0.0825'), 2)
        total = round(subtotal + tax_estimate, 2)
        return {
            'cart_count': total_count,
            'cart_subtotal': subtotal,
            'cart_tax': tax_estimate,
            'cart_total': total,
        }
    return {
        'cart_count': 0,
        'cart_subtotal': Decimal('0.00'),
        'cart_tax': Decimal('0.00'),
        'cart_total': Decimal('0.00'),
    }
