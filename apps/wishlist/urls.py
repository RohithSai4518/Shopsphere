from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist_view, name='wishlist_list'),
    path('add/<str:product_id>/', views.add_to_wishlist_view, name='add_to_wishlist'),
    path('price-alert/<str:product_id>/', views.set_price_alert_view, name='set_price_alert'),
    path('stock-alert/<str:variant_id>/', views.set_stock_alert_view, name='set_stock_alert'),
]
