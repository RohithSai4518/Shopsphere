from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import SupportTicket, SupportMessage, FAQCategory, FAQArticle
from .services import SupportService
from .knowledgebase import KnowledgeBaseService

def help_center_view(request):
    """Universal customer Help Center and searchable Knowledge Base."""
    query = request.GET.get('q', '').strip()
    selected_cat_slug = request.GET.get('category', '').strip()

    if query:
        search_results = KnowledgeBaseService.search_faqs(query)
        categories = KnowledgeBaseService.get_all_categories()
        return render(request, 'support/help_center.html', {
            'query': query,
            'search_results': search_results,
            'categories': categories,
            'is_search': True
        })

    categories = KnowledgeBaseService.get_all_categories()
    selected_category = None
    if selected_cat_slug:
        selected_category = FAQCategory.objects.filter(slug=selected_cat_slug).first()

    return render(request, 'support/help_center.html', {
        'categories': categories,
        'selected_category': selected_category,
        'is_search': False
    })


def faq_helpful_api(request, article_id):
    """Upvotes an article helpful count via AJAX."""
    if request.method == 'POST':
        success, count = KnowledgeBaseService.vote_helpful(article_id)
        return JsonResponse({'success': success, 'helpful_count': count})
    return JsonResponse({'error': 'POST required'}, status=405)


@login_required
def ticket_list_view(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})


@login_required
def create_ticket_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        category = request.POST.get('category', 'GENERAL')
        priority = request.POST.get('priority', 'MEDIUM')
        message = request.POST.get('message', '').strip()

        ticket = SupportService.create_ticket(
            user=request.user,
            subject=subject,
            category=category,
            priority=priority,
            initial_message=message
        )
        messages.success(request, f'Support Ticket #{ticket.ticket_number} created successfully.')
        return redirect('support:ticket_detail', ticket_id=ticket.id)

    return render(request, 'support/create_ticket.html')


@login_required
def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    messages_list = ticket.messages.filter(is_internal_note=False).select_related('sender')

    if request.method == 'POST':
        reply = request.POST.get('reply', '').strip()
        if reply:
            SupportService.add_message(ticket, request.user, reply)
            messages.success(request, 'Reply submitted.')
            return redirect('support:ticket_detail', ticket_id=ticket.id)

    return render(request, 'support/ticket_detail.html', {'ticket': ticket, 'messages_list': messages_list})
