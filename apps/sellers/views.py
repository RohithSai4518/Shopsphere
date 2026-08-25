from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Seller
from .services import SellerService, SellerAnalyticsService
from apps.rbac.decorators import role_required
from apps.catalog.models import Product, ProductVariant, Category, Brand
from apps.inventory.models import Inventory
from apps.inventory.services import InventoryService
from apps.orders.models import OrderItem

@login_required
@role_required('SELLER', 'ADMIN')
def seller_dashboard_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    metrics = SellerAnalyticsService.calculate_seller_metrics(seller)
    recent_items = OrderItem.objects.filter(seller=seller).select_related('order', 'variant__product').order_by('-created_at')[:10]

    return render(request, 'sellers/dashboard.html', {
        'seller': seller,
        'metrics': metrics,
        'recent_items': recent_items
    })

@login_required
@role_required('SELLER', 'ADMIN')
def seller_products_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    products = Product.objects.filter(seller=seller).select_related('category', 'brand').prefetch_related('variants__inventory')
    return render(request, 'sellers/products.html', {'seller': seller, 'products': products})

@login_required
@role_required('SELLER', 'ADMIN')
def seller_product_create_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        cat_id = request.POST.get('category')
        brand_id = request.POST.get('brand')
        description = request.POST.get('description', '').strip()
        base_price = request.POST.get('base_price', '0.00')

        category = get_object_or_404(Category, id=cat_id)
        brand = Brand.objects.filter(id=brand_id).first()

        product = Product.objects.create(
            seller=seller,
            category=category,
            brand=brand,
            name=name,
            description=description,
            base_price=base_price,
            status='PUBLISHED'
        )

        variant = ProductVariant.objects.create(
            product=product,
            sku=f"SKU-{seller.id[:4].upper()}-{product.id[:6].upper()}",
            variant_name='Standard Edition',
            price_override=base_price
        )

        InventoryService.restock_variant(variant, 50, notes='Initial Seller Listing Restock')

        messages.success(request, f"Product '{product.name}' created and published successfully!")
        return redirect('sellers:products')

    return render(request, 'sellers/product_form.html', {'categories': categories, 'brands': brands})

@login_required
@role_required('SELLER', 'ADMIN')
def seller_orders_view(request):
    seller = get_object_or_404(Seller, user=request.user)
    items = OrderItem.objects.filter(seller=seller).select_related('order', 'variant__product').order_by('-created_at')
    return render(request, 'sellers/orders.html', {'items': items})

@login_required
@role_required('SELLER', 'ADMIN')
def fulfill_order_item_view(request, item_id):
    seller = get_object_or_404(Seller, user=request.user)
    item = get_object_or_404(OrderItem, id=item_id, seller=seller)
    item.item_status = 'SHIPPED'
    item.save()

    # Deduct Stock
    InventoryService.deduct_stock_for_shipment(item.variant, item.quantity, reference_id=item.order.id)
    messages.success(request, f"Item '{item.variant.sku}' marked as SHIPPED!")
    return redirect('sellers:orders')
