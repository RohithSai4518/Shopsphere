from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('deals/', views.deals_view, name='deals'),
    path('deals/claim/<str:deal_id>/', views.claim_deal_api, name='claim_deal'),
    path('api/suggestions/', views.search_suggestions_api, name='search_suggestions'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('compare/', views.product_compare_view, name='compare'),
    path('product/<str:product_id>/ask/', views.ask_question_view, name='ask_question'),
    path('question/<str:question_id>/answer/', views.answer_question_view, name='answer_question'),
    path('qa/vote/<str:item_type>/<str:item_id>/', views.vote_qa_view, name='vote_qa'),
]
