from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Category, Brand, Product, ProductVariant, ProductBundle, ProductQuestion, ProductAnswer, Tag
from .services import CatalogService
from .deals import LightningDeal, DealService
from .qa import QAService
from apps.analytics.services import AnalyticsService

def home_view(request):
    base_qs = Product.objects.filter(status='PUBLISHED').select_related('category', 'brand').prefetch_related('images', 'variants')
    featured_products = list(base_qs.filter(is_featured=True)[:8])
    if not featured_products:
        featured_products = list(base_qs[:8])
    bestseller_products = list(base_qs.filter(is_bestseller=True)[:4])
    if not bestseller_products:
        bestseller_products = list(base_qs.order_by('-discount_percent', '-created_at')[:4])
    trending_products = list(base_qs.filter(is_trending=True)[:4])
    if not trending_products:
        trending_products = list(base_qs.order_by('-created_at')[:4])
    new_arrivals = list(base_qs.order_by('-created_at')[:4])
    categories = list(Category.objects.filter(is_active=True, parent__isnull=True).order_by('display_order', 'name'))
    bundles = list(ProductBundle.objects.filter(is_active=True)[:3])
    live_deals = DealService.get_live_deals(limit=4)

    return render(request, 'catalog/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'bestseller_products': bestseller_products,
        'trending_products': trending_products,
        'new_arrivals': new_arrivals,
        'product_count': Product.objects.filter(status='PUBLISHED').count(),
        'category_count': Category.objects.filter(is_active=True).count(),
        'bundles': bundles,
        'live_deals': live_deals
    })

def product_list_view(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    brand_id = request.GET.get('brand', '').strip()
    tag_slug = request.GET.get('tag', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'newest')

    products = CatalogService.search_products(
        query=query,
        category_slug=category_slug,
        brand_id=brand_id,
        tag_slug=tag_slug,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by
    )

    if query:
        AnalyticsService.record_search_query(request.user, query, products.count())

    facets = CatalogService.get_faceted_counts(products)
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by('display_order', 'name')
    brands = Brand.objects.all()[:20]
    tags = Tag.objects.all()[:10]

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'tags': tags,
        'facets': facets,
        'query': query,
        'category_slug': category_slug,
        'brand_id': brand_id,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'sort_by': sort_by,
    })

def search_suggestions_api(request):
    query = request.GET.get('q', '').strip()
    suggestions = CatalogService.get_enhanced_search_suggestions(query)
    return JsonResponse(suggestions)

def deals_view(request):
    category_slug = request.GET.get('category')
    deals = DealService.get_live_deals(category_slug=category_slug, limit=30)
    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by('name')
    return render(request, 'catalog/deals.html', {
        'deals': deals,
        'categories': categories,
        'selected_category': category_slug
    })

@login_required
def claim_deal_api(request, deal_id):
    if request.method == 'POST':
        success, msg = DealService.claim_deal(request.user, deal_id)
        return JsonResponse({'success': success, 'message': msg})
    return JsonResponse({'error': 'POST required'}, status=405)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, status='PUBLISHED')
    variants = product.variants.all()
    specs = product.specifications.all()
    reviews = product.reviews.filter(status='APPROVED').select_related('user')
    qa_query = request.GET.get('qa_q', '').strip()
    questions = QAService.get_product_qa(product, query=qa_query, limit=15)
    recommendations = CatalogService.get_recommendations_for_product(product, limit=4)
    active_deal = DealService.get_deal_for_product(product)

    # Record View Analytics
    AnalyticsService.record_product_view(request.user, product)

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'variants': variants,
        'specs': specs,
        'reviews': reviews,
        'questions': questions,
        'qa_query': qa_query,
        'recommendations': recommendations,
        'active_deal': active_deal
    })

def product_compare_view(request):
    product_ids = request.GET.getlist('id')
    comparison_data = CatalogService.get_product_comparison_matrix(product_ids)
    all_products = Product.objects.filter(status='PUBLISHED')[:30]

    return render(request, 'catalog/compare.html', {
        'comparison': comparison_data,
        'all_products': all_products,
        'selected_ids': product_ids
    })

@login_required
def ask_question_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '').strip()
        try:
            QAService.ask_question(product, request.user, question_text)
            messages.success(request, 'Your question has been posted to the community!')
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('catalog:product_detail', slug=product.slug)

@login_required
def answer_question_view(request, question_id):
    question = get_object_or_404(ProductQuestion, id=question_id)
    if request.method == 'POST':
        answer_text = request.POST.get('answer_text', '').strip()
        try:
            QAService.answer_question(question, request.user, answer_text)
            messages.success(request, 'Thank you for answering this question!')
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('catalog:product_detail', slug=question.product.slug)

@login_required
def vote_qa_view(request, item_type, item_id):
    if request.method == 'POST':
        if item_type == 'question':
            q = get_object_or_404(ProductQuestion, id=item_id)
            voted = QAService.vote_question(q, request.user)
            return JsonResponse({'success': True, 'voted': voted})
        elif item_type == 'answer':
            a = get_object_or_404(ProductAnswer, id=item_id)
            is_helpful = request.POST.get('helpful', 'true').lower() == 'true'
            vote = QAService.vote_answer(a, request.user, is_helpful=is_helpful)
            return JsonResponse({'success': True, 'is_helpful': vote.is_helpful})
    return JsonResponse({'error': 'POST required'}, status=405)
