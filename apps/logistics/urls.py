from django.urls import path
from . import views

app_name = 'logistics'

urlpatterns = [
    path('track/', views.tracking_portal, name='track_search'),
    path('track/<str:tracking_number>/', views.tracking_portal, name='track_detail'),
    path('hub/', views.warehouse_dashboard, name='hub_dashboard_default'),
    path('hub/<str:hub_id>/', views.warehouse_dashboard, name='hub_dashboard'),
    path('packing-slip/<str:parcel_id>/', views.packing_slip, name='packing_slip'),
    path('api/track/<str:tracking_number>/', views.api_tracking_status, name='api_tracking'),
]
