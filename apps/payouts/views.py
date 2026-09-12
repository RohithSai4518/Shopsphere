from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import csv
from .models import SellerEscrowAccount, EscrowTransaction, PayoutBatch, PayoutItem, SellerBankAccount
from apps.sellers.models import Seller
from .services import EscrowService

@login_required
def seller_financial_dashboard(request):
    try:
        seller = Seller.objects.get(user=request.user)
    except Seller.DoesNotExist:
        # Fallback to first seller for demo or testing
        seller = Seller.objects.first()
        if not seller:
            messages.error(request, "No merchant profile found for this account.")
            return redirect('catalog:home')

    account = EscrowService.get_or_create_account(seller)
    recent_transactions = EscrowTransaction.objects.filter(account=account).order_by('-created_at')[:20]
    payout_history = PayoutItem.objects.filter(seller=seller).select_related('batch').order_by('-created_at')[:10]
    bank_account = SellerBankAccount.objects.filter(seller=seller, is_primary=True).first()

    return render(request, 'payouts/seller_financial_dashboard.html', {
        'seller': seller,
        'account': account,
        'transactions': recent_transactions,
        'payout_history': payout_history,
        'bank_account': bank_account
    })

@login_required
def statement_detail(request, batch_id):
    batch = get_object_or_404(PayoutBatch, id=batch_id)
    items = batch.items.select_related('seller', 'bank_account').all()
    
    # Check if CSV export requested
    if request.GET.get('format') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="payout_statement_{batch.batch_reference}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Batch Ref', 'Seller', 'Bank Account', 'Gross Sales ($)', 'Platform Fee ($)', 'Net Payout ($)', 'Status', 'Transfer Ref'])
        for item in items:
            bank_str = f"{item.bank_account.bank_name} (*{item.bank_account.account_number_last4})" if item.bank_account else "Not Specified"
            writer.writerow([
                batch.batch_reference,
                item.seller.business_name,
                bank_str,
                item.gross_sales,
                item.platform_fee,
                item.net_payout,
                'Settled' if item.is_settled else 'Pending',
                item.transfer_reference
            ])
        return response

    return render(request, 'payouts/statement_detail.html', {
        'batch': batch,
        'items': items
    })
