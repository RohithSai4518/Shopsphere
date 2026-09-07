from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('dashboard/', views.governance_dashboard_view, name='dashboard'),
    path('sellers/', views.manage_sellers_view, name='manage_sellers'),
    path('sellers/<str:seller_id>/approve/', views.approve_seller_view, name='approve_seller'),
    path('products/', views.manage_products_view, name='manage_products'),
    path('products/<str:product_id>/moderate/', views.moderate_product_view, name='moderate_product'),
    path('reviews/', views.manage_reviews_view, name='manage_reviews'),
    path('reviews/<str:review_id>/moderate/', views.moderate_review_view, name='moderate_review'),
    path('users/', views.manage_users_view, name='manage_users'),
    path('users/<str:user_id>/toggle-status/', views.toggle_user_status_view, name='toggle_user_status'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
]
