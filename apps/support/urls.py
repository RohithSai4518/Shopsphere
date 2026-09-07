from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.help_center_view, name='help_center'),
    path('faq/<str:article_id>/helpful/', views.faq_helpful_api, name='faq_helpful'),
    path('tickets/', views.ticket_list_view, name='ticket_list'),
    path('tickets/new/', views.create_ticket_view, name='create_ticket'),
    path('tickets/<str:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
]
