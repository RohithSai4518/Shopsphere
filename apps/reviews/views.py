from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review, ReviewVote
from apps.catalog.models import Product

@login_required
def add_review_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '')
        comment = request.POST.get('comment', '')

        Review.objects.update_or_create(
            product=product,
            user=request.user,
            defaults={
                'rating': rating,
                'title': title,
                'comment': comment,
                'is_verified_purchase': True,
                'status': 'APPROVED'
            }
        )
        messages.success(request, 'Review submitted successfully!')
    return redirect('catalog:product_detail', slug=product.slug)
