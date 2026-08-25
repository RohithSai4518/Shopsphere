from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ReturnRequest
from .services import ReturnService
from apps.orders.models import Order, OrderItem

@login_required
def return_list_view(request):
    returns = ReturnRequest.objects.filter(user=request.user).select_related('order', 'order_item__variant__product')
    return render(request, 'returns/return_list.html', {'returns': returns})

@login_required
def create_return_view(request, order_item_id):
    order_item = get_object_or_404(OrderItem, id=order_item_id, order__user=request.user)
    if request.method == 'POST':
        reason = request.POST.get('reason', 'DEFECTIVE')
        comments = request.POST.get('comments', '').strip()
        rma = ReturnService.submit_return_request(
            order=order_item.order,
            order_item=order_item,
            user=request.user,
            reason=reason,
            comments=comments
        )
        messages.success(request, f'RMA Return Request #{rma.id} submitted.')
        return redirect('returns:return_list')

    return render(request, 'returns/create_return.html', {'order_item': order_item})
