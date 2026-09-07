from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail_view, name='cart_detail'),
    path('add/<str:variant_id>/', views.add_to_cart_view, name='add_to_cart'),
    path('update/<str:item_id>/', views.update_cart_view, name='update_cart'),
    path('remove/<str:item_id>/', views.remove_cart_view, name='remove_cart'),
    path('remove-item/<str:item_id>/', views.remove_cart_view, name='remove_from_cart'),
    path('save-for-later/', views.save_for_later_view, name='save_for_later'),
    path('restore/<str:saved_cart_id>/', views.restore_saved_cart_view, name='restore_saved_cart'),
]
