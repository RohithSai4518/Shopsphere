from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .services import CartService
from .models import SavedCart
from apps.promotions.models import Coupon
from apps.promotions.services import PromotionService, CouponValidationError

@login_required
def cart_detail_view(request):
    coupon_code = request.GET.get('coupon', '').strip()
    coupon = None
    coupon_error = None

    if coupon_code:
        try:
            cart_summary = CartService.calculate_cart_summary(request.user)
            coupon, discount = PromotionService.validate_and_apply_coupon(
                code=coupon_code,
                subtotal=cart_summary['subtotal'],
                user=request.user
            )
        except CouponValidationError as err:
            coupon_error = str(err)

    cart_summary = CartService.calculate_cart_summary(request.user, coupon=coupon)
    saved_carts = SavedCart.objects.filter(user=request.user)

    return render(request, 'cart/cart_detail.html', {
        'cart': cart_summary,
        'saved_carts': saved_carts,
        'coupon': coupon,
        'coupon_error': coupon_error
    })

@login_required
def add_to_cart_view(request, variant_id):
    quantity = int(request.POST.get('quantity', 1))
    CartService.add_to_cart(request.user, variant_id, quantity)
    messages.success(request, 'Item added to your shopping cart.')
    return redirect('cart:cart_detail')

@login_required
def update_cart_view(request, item_id):
    quantity = int(request.POST.get('quantity', 1))
    CartService.update_cart_item(request.user, item_id, quantity)
    messages.info(request, 'Cart updated.')
    return redirect('cart:cart_detail')

@login_required
def remove_cart_view(request, item_id):
    CartService.remove_cart_item(request.user, item_id)
    messages.info(request, 'Item removed from cart.')
    return redirect('cart:cart_detail')

@login_required
def save_for_later_view(request):
    saved_cart = CartService.save_cart_for_later(request.user)
    if saved_cart:
        messages.success(request, 'Your active cart has been saved for later!')
    return redirect('cart:cart_detail')

@login_required
def restore_saved_cart_view(request, saved_cart_id):
    CartService.restore_saved_cart(request.user, saved_cart_id)
    messages.success(request, 'Saved cart restored to your active shopping cart.')
    return redirect('cart:cart_detail')
