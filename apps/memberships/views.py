from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import MembershipTier, UserMembership, RewardWallet, RewardTransaction, SubscriptionPlan
from .services import MembershipService, RewardWalletService

def prime_landing(request):
    tiers = MembershipTier.objects.filter(is_active=True).order_by('price')
    user_membership = None
    is_prime = False
    
    if request.user.is_authenticated:
        user_membership = UserMembership.objects.filter(user=request.user).first()
        is_prime = MembershipService.is_user_prime(request.user)
        
    return render(request, 'memberships/prime_landing.html', {
        'tiers': tiers,
        'user_membership': user_membership,
        'is_prime': is_prime
    })

@login_required
def enroll_prime(request, tier_code):
    membership = MembershipService.enroll_user(request.user, tier_code)
    messages.success(request, f"Welcome to {membership.tier.name}! Enjoy fast free delivery and 5% back on all purchases.")
    return redirect('memberships:prime_landing')

@login_required
def wallet_dashboard(request):
    wallet = RewardWalletService.get_or_create_wallet(request.user)
    transactions = RewardTransaction.objects.filter(wallet=wallet).order_by('-created_at')[:30]
    is_prime = MembershipService.is_user_prime(request.user)
    
    return render(request, 'memberships/wallet.html', {
        'wallet': wallet,
        'transactions': transactions,
        'is_prime': is_prime
    })

@login_required
def subscriptions_dashboard(request):
    subscriptions = SubscriptionPlan.objects.filter(user=request.user).select_related('variant', 'variant__product').order_by('-created_at')
    return render(request, 'memberships/subscriptions.html', {
        'subscriptions': subscriptions
    })

@login_required
def toggle_subscription(request, sub_id):
    sub = get_object_or_404(SubscriptionPlan, id=sub_id, user=request.user)
    action = request.POST.get('action', '')
    if action == 'pause':
        sub.status = 'PAUSED'
        messages.info(request, f"Auto-delivery for {sub.variant.sku} has been paused.")
    elif action == 'resume':
        sub.status = 'ACTIVE'
        messages.success(request, f"Auto-delivery for {sub.variant.sku} has been resumed.")
    elif action == 'cancel':
        sub.status = 'CANCELLED'
        messages.warning(request, f"Subscription for {sub.variant.sku} has been cancelled.")
    sub.save()
    return redirect('memberships:subscriptions')
