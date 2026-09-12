from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('for-you/', views.for_you_feed, name='for_you'),
    path('bundles/<str:product_id>/', views.bundle_explorer, name='bundle_explorer'),
    path('api/similar/<str:product_id>/', views.api_similar, name='api_similar'),
]
