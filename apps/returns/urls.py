from django.urls import path
from . import views

app_name = 'returns'

urlpatterns = [
    path('', views.return_list_view, name='return_list'),
    path('request/<str:order_item_id>/', views.create_return_view, name='create_return'),
]
