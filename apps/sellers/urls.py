from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    path('dashboard/', views.seller_dashboard_view, name='dashboard'),
    path('products/', views.seller_products_view, name='products'),
    path('products/new/', views.seller_product_create_view, name='product_create'),
    path('orders/', views.seller_orders_view, name='orders'),
    path('orders/<str:item_id>/fulfill/', views.fulfill_order_item_view, name='fulfill_item'),
]
