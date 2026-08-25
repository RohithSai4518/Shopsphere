from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('status/', views.inventory_status_view, name='status'),
]
