from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.ticket_list_view, name='ticket_list'),
    path('new/', views.create_ticket_view, name='create_ticket'),
    path('<str:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
]
