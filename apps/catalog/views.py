from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Category, Brand, Product, ProductVariant, ProductBundle, ProductQuestion, ProductAnswer, Tag
from .services import CatalogService
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

    return render(request, 'catalog/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'bestseller_products': bestseller_products,
        'trending_products': trending_products,
        'new_arrivals': new_arrivals,
        'product_count': Product.objects.filter(status='PUBLISHED').count(),
        'category_count': Category.objects.filter(is_active=True).count(),
        'bundles': bundles
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

    categories = Category.objects.filter(is_active=True, parent__isnull=True).order_by('display_order', 'name')
    brands = Brand.objects.all()[:20]
    tags = Tag.objects.all()[:10]

    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'brands': brands,
        'tags': tags,
        'query': query,
        'category_slug': category_slug,
        'brand_id': brand_id,
        'sort_by': sort_by,
    })

def search_suggestions_api(request):
    query = request.GET.get('q', '').strip()
    suggestions = CatalogService.get_search_suggestions(query)
    return JsonResponse({'suggestions': suggestions})

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, status='PUBLISHED')
    variants = product.variants.all()
    specs = product.specifications.all()
    reviews = product.reviews.filter(status='APPROVED').select_related('user')
    questions = product.questions.filter(is_approved=True).prefetch_related('answers')
    recommendations = CatalogService.get_recommendations_for_product(product, limit=4)

    # Record View Analytics
    AnalyticsService.record_product_view(request.user, product)

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'variants': variants,
        'specs': specs,
        'reviews': reviews,
        'questions': questions,
        'recommendations': recommendations
    })

def product_compare_view(request):
    product_ids = request.GET.getlist('id')
    products = Product.objects.filter(id__in=product_ids, status='PUBLISHED')
    return render(request, 'catalog/compare.html', {'products': products})

@login_required
def ask_question_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        question_text = request.POST.get('question_text', '').strip()
        if question_text:
            ProductQuestion.objects.create(
                product=product,
                user=request.user,
                question_text=question_text
            )
            messages.success(request, 'Your question has been submitted!')
    return redirect('catalog:product_detail', slug=product.slug)

@login_required
def answer_question_view(request, question_id):
    question = get_object_or_404(ProductQuestion, id=question_id)
    if request.method == 'POST':
        answer_text = request.POST.get('answer_text', '').strip()
        if answer_text:
            is_seller = (request.user == question.product.seller.user)
            ProductAnswer.objects.create(
                question=question,
                user=request.user,
                answer_text=answer_text,
                is_seller_answer=is_seller
            )
            messages.success(request, 'Answer submitted successfully.')
    return redirect('catalog:product_detail', slug=question.product.slug)
