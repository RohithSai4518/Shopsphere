from django.urls import path
from . import views

app_name = 'administration'

urlpatterns = [
    path('dashboard/', views.governance_dashboard_view, name='dashboard'),
    path('sellers/', views.manage_sellers_view, name='manage_sellers'),
    path('sellers/<str:seller_id>/approve/', views.approve_seller_view, name='approve_seller'),
    path('products/', views.manage_products_view, name='manage_products'),
    path('products/<str:product_id>/moderate/', views.moderate_product_view, name='moderate_product'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
]
