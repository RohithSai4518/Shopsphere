import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from .models import Order
from .services import OrderService, OrderProcessingError
from .invoicing import InvoiceService
from apps.cart.models import CartItem
from apps.accounts.models import Address
from apps.promotions.models import Coupon
from apps.promotions.services import PromotionService

@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_detail')

    addresses = request.user.addresses.all()
    saved_cards = request.user.saved_payment_methods.all()
    coupon_code = request.GET.get('coupon', '').strip()
    coupon = None
    if coupon_code:
        coupon = Coupon.objects.filter(code__iexact=coupon_code, is_active=True).first()

    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        address_obj = Address.objects.filter(id=address_id, user=request.user).first()
        if not address_obj:
            messages.error(request, 'Please select a valid shipping address.')
            return redirect('orders:checkout')

        address_json = f'{{"full_name": "{address_obj.full_name}", "street": "{address_obj.street_address_1}", "city": "{address_obj.city}", "state": "{address_obj.state}", "postal_code": "{address_obj.postal_code}", "country": "{address_obj.country}"}}'
        
        delivery_speed = request.POST.get('delivery_speed', 'STANDARD')
        is_gift = request.POST.get('is_gift') == 'on'
        gift_message = request.POST.get('gift_message', '').strip()
        gift_wrap_type = request.POST.get('gift_wrap_type', 'NONE')
        idempotency_key = request.POST.get('idempotency_key', '').strip() or f"idemp_{uuid.uuid4().hex}"

        try:
            order = OrderService.process_checkout(
                user=request.user,
                cart_items=cart_items,
                shipping_address=address_json,
                coupon=coupon,
                delivery_speed=delivery_speed,
                is_gift=is_gift,
                gift_message=gift_message,
                gift_wrap_type=gift_wrap_type,
                idempotency_key=idempotency_key
            )
            messages.success(request, f"Order #{order.order_number} confirmed! Thank you for choosing ShopSphere.")
            return redirect('orders:order_detail', order_id=order.id)
        except OrderProcessingError as err:
            messages.error(request, f"Checkout failed: {err}")

    # Generate fresh idempotency token for this session/checkout
    form_idempotency_key = f"idemp_{uuid.uuid4().hex[:16]}"
    subtotal = sum(i.subtotal for i in cart_items)
    discount = coupon.calculate_discount(subtotal) if coupon else Decimal('0.00')
    taxable = max(Decimal('0.00'), subtotal - discount)
    tax = round(taxable * Decimal('0.0825'), 2)
    total = round(taxable + tax, 2)

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'addresses': addresses,
        'saved_cards': saved_cards,
        'coupon': coupon,
        'subtotal': subtotal,
        'discount': discount,
        'tax': tax,
        'total': total,
        'idempotency_key': form_idempotency_key
    })

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__variant__product').order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    shipments = order.shipments.prefetch_related('events')
    return render(request, 'orders/order_detail.html', {'order': order, 'shipments': shipments})

@login_required
def order_invoice_view(request, order_id):
    """Generates official tax invoice receipt page with print styling."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    invoice_context = InvoiceService.get_invoice_context(order)
    return render(request, 'orders/invoice.html', invoice_context)

@login_required
def cancel_order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    try:
        OrderService.update_order_status(order, 'CANCELLED', user=request.user, notes='Cancelled by customer')
        messages.info(request, f'Order #{order.order_number} has been cancelled.')
    except OrderProcessingError as err:
        messages.error(request, str(err))
    return redirect('orders:order_detail', order_id=order.id)
