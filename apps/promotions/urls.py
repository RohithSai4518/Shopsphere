from django.urls import path
from . import views

app_name = 'promotions'

urlpatterns = [
    path('list/', views.promotion_list_view, name='list'),
]
