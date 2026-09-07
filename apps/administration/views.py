from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.rbac.decorators import role_required
from apps.accounts.models import User
from apps.sellers.models import Seller
from apps.sellers.services import SellerService
from apps.catalog.models import Product
from apps.catalog.services import CatalogService
from apps.orders.models import Order
from apps.reviews.models import Review
from apps.audit.models import SecurityAuditLog
from apps.analytics.services import AnalyticsService

@login_required
@role_required('ADMIN')
def governance_dashboard_view(request):
    total_customers = User.objects.filter(role='CUSTOMER').count()
    total_sellers = Seller.objects.count()
    pending_sellers = Seller.objects.filter(status='PENDING').count()
    pending_reviews = Review.objects.filter(status='PENDING').count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    audit_logs = SecurityAuditLog.objects.select_related('user')[:15]
    platform_metrics = AnalyticsService.calculate_platform_daily_metrics()

    return render(request, 'administration/dashboard.html', {
        'total_customers': total_customers,
        'total_sellers': total_sellers,
        'pending_sellers': pending_sellers,
        'pending_reviews': pending_reviews,
        'total_products': total_products,
        'total_orders': total_orders,
        'audit_logs': audit_logs,
        'platform_metrics': platform_metrics
    })

@login_required
@role_required('ADMIN')
def manage_sellers_view(request):
    sellers = Seller.objects.select_related('user').order_by('-created_at')
    return render(request, 'administration/sellers.html', {'sellers': sellers})

@login_required
@role_required('ADMIN')
def approve_seller_view(request, seller_id):
    seller = get_object_or_404(Seller, id=seller_id)
    SellerService.approve_seller(seller, approved_by=request.user)
    messages.success(request, f"Merchant '{seller.business_name}' APPROVED.")
    return redirect('administration:manage_sellers')

@login_required
@role_required('ADMIN')
def manage_products_view(request):
    products = Product.objects.select_related('seller', 'category').order_by('-created_at')
    return render(request, 'administration/products.html', {'products': products})

@login_required
@role_required('ADMIN')
def moderate_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    new_status = request.POST.get('status', 'PUBLISHED')
    reason = request.POST.get('reason', 'Admin Governance Action')

    CatalogService.moderate_product(product, new_status, moderator=request.user, reason=reason)
    messages.info(request, f"Product '{product.name}' status updated to '{new_status}'.")
    return redirect('administration:manage_products')

@login_required
@role_required('ADMIN')
def manage_reviews_view(request):
    """Review moderation console for verifying customer feedback."""
    status_filter = request.GET.get('status', 'ALL')
    if status_filter == 'PENDING':
        reviews = Review.objects.filter(status='PENDING').select_related('product', 'user').order_by('-created_at')
    elif status_filter in ['APPROVED', 'REJECTED']:
        reviews = Review.objects.filter(status=status_filter).select_related('product', 'user').order_by('-created_at')
    else:
        reviews = Review.objects.select_related('product', 'user').order_by('-created_at')[:50]

    return render(request, 'administration/reviews.html', {
        'reviews': reviews,
        'status_filter': status_filter
    })

@login_required
@role_required('ADMIN')
def moderate_review_view(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    action = request.POST.get('action')

    if action == 'approve':
        review.status = 'APPROVED'
        review.save(update_fields=['status'])
        messages.success(request, f"Review #{review.id[:8]} approved and visible to customers.")
    elif action == 'reject':
        review.status = 'REJECTED'
        review.save(update_fields=['status'])
        messages.warning(request, f"Review #{review.id[:8]} rejected and hidden from storefront.")

    SecurityAuditLog.objects.create(
        user=request.user,
        action=f"REVIEW_MODERATION_{action.upper()}",
        module='reviews',
        entity_type='Review',
        entity_id=review.id
    )

    return redirect('administration:manage_reviews')

@login_required
@role_required('ADMIN')
def manage_users_view(request):
    """Platform user governance and account status management."""
    users = User.objects.order_by('-created_at')[:60]
    return render(request, 'administration/users.html', {'users': users})

@login_required
@role_required('ADMIN')
def toggle_user_status_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "Cannot modify your own administrator account status.")
        return redirect('administration:manage_users')

    target_user.is_active = not target_user.is_active
    target_user.status = 'ACTIVE' if target_user.is_active else 'SUSPENDED'
    target_user.save(update_fields=['is_active', 'status'])

    SecurityAuditLog.objects.create(
        user=request.user,
        action='USER_STATUS_TOGGLED',
        module='accounts',
        entity_type='User',
        entity_id=target_user.id,
        metadata_json=f'{{"is_active": {target_user.is_active}}}'
    )

    messages.info(request, f"User '{target_user.email}' status is now {'ACTIVE' if target_user.is_active else 'SUSPENDED'}.")
    return redirect('administration:manage_users')

@login_required
@role_required('ADMIN')
def audit_logs_view(request):
    logs = SecurityAuditLog.objects.select_related('user').order_by('-created_at')[:100]
    return render(request, 'administration/audit_logs.html', {'logs': logs})
