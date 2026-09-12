from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ProductSimilarity, FrequentlyBoughtTogether
from .services import RecommendationEngine
from apps.catalog.models import Product

def for_you_feed(request):
    recommended_products = RecommendationEngine.get_personalized_feed(request.user, limit=16)
    return render(request, 'recommendations/for_you.html', {
        'products': recommended_products
    })

def bundle_explorer(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    bundle_data = RecommendationEngine.get_frequently_bought_bundle(product)
    similar_products = RecommendationEngine.get_similar_products(product, limit=4)
    
    return render(request, 'recommendations/bundles.html', {
        'product': product,
        'bundle_data': bundle_data,
        'similar_products': similar_products
    })

def api_similar(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    similar = RecommendationEngine.get_similar_products(product, limit=6)
    data = [{
        'id': p.id,
        'title': p.name,
        'name': p.name,
        'slug': p.slug,
        'category': p.category.name if p.category else 'General',
        'price': str(p.effective_price),
    } for p in similar]
    return JsonResponse({'status': 'success', 'similar_products': data})
