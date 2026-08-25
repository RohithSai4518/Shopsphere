from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('history/', views.order_history_view, name='order_history'),
    path('<str:order_id>/', views.order_detail_view, name='order_detail'),
    path('<str:order_id>/cancel/', views.cancel_order_view, name='cancel_order'),
]
