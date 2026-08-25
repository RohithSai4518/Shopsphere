from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist, WishlistItem, PriceAlert, BackInStockAlert
from .services import WishlistService
from apps.catalog.models import Product, ProductVariant

@login_required
def wishlist_view(request):
    wishlists = Wishlist.objects.filter(user=request.user).prefetch_related('items__product')
    price_alerts = PriceAlert.objects.filter(user=request.user).select_related('product')
    stock_alerts = BackInStockAlert.objects.filter(user=request.user).select_related('variant__product')

    return render(request, 'wishlist/wishlist_list.html', {
        'wishlists': wishlists,
        'price_alerts': price_alerts,
        'stock_alerts': stock_alerts
    })

@login_required
def add_to_wishlist_view(request, product_id):
    WishlistService.add_to_wishlist(request.user, product_id)
    messages.success(request, 'Product saved to your wishlist!')
    return redirect('wishlist:wishlist_list')

@login_required
def set_price_alert_view(request, product_id):
    if request.method == 'POST':
        target_price = request.POST.get('target_price', '0.00')
        WishlistService.set_price_alert(request.user, product_id, target_price)
        messages.success(request, f'Price alert set for target price of ${target_price}.')
    return redirect('wishlist:wishlist_list')

@login_required
def set_stock_alert_view(request, variant_id):
    WishlistService.set_back_in_stock_alert(request.user, variant_id)
    messages.success(request, 'Stock alert registered! We will notify you when back in stock.')
    return redirect('wishlist:wishlist_list')
