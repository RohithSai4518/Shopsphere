from django.urls import path
from . import views

app_name = 'payouts'

urlpatterns = [
    path('dashboard/', views.seller_financial_dashboard, name='dashboard'),
    path('statement/<str:batch_id>/', views.statement_detail, name='statement_detail'),
]
