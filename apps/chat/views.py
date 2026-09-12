from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import ChatChannel, ChatMessage
from .services import ChatEngine
from apps.orders.models import Order

@login_required
def chat_room(request, channel_code=None):
    channel = None
    if channel_code:
        channel = get_object_or_404(ChatChannel, channel_code=channel_code)
    else:
        order_id = request.GET.get('order_id')
        order = Order.objects.filter(id=order_id).first() if order_id else None
        channel = ChatEngine.get_or_create_support_channel(request.user, order=order)

    chat_messages = channel.messages.all()
    return render(request, 'chat/chat_room.html', {
        'channel': channel,
        'chat_messages': chat_messages
    })

@login_required
def agent_workspace(request):
    open_channels = ChatChannel.objects.filter(
        status__in=['OPEN', 'WAITING_ON_AGENT']
    ).select_related('customer', 'order', 'assigned_agent')
    
    resolved_channels = ChatChannel.objects.filter(
        status='RESOLVED'
    ).select_related('customer', 'order')[:15]
    
    return render(request, 'chat/agent_workspace.html', {
        'open_channels': open_channels,
        'resolved_channels': resolved_channels
    })

@login_required
def api_send_message(request, channel_code):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'POST required'}, status=405)
        
    channel = get_object_or_404(ChatChannel, channel_code=channel_code)
    body = request.POST.get('body', '').strip()
    if not body:
        return JsonResponse({'status': 'error', 'message': 'Empty message'}, status=400)
        
    msg = ChatEngine.post_user_message(channel, request.user, body)
    return redirect('chat:chat_room_detail', channel_code=channel.channel_code)

@login_required
def api_poll_messages(request, channel_code):
    channel = get_object_or_404(ChatChannel, channel_code=channel_code)
    last_id = request.GET.get('last_id')
    
    msgs = channel.messages.all()
    if last_id:
        msgs = msgs.filter(id__gt=last_id)
        
    data = [{
        'id': m.id,
        'sender_role': m.sender_role,
        'sender_name': m.sender.username if m.sender else 'ShopSphere Assistant',
        'body': m.body,
        'created_at': m.created_at.strftime('%I:%M %p')
    } for m in msgs]
    
    return JsonResponse({'status': 'success', 'messages': data})
