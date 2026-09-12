from django.urls import path
from . import views

app_name = 'memberships'

urlpatterns = [
    path('prime/', views.prime_landing, name='prime_landing'),
    path('prime/enroll/<str:tier_code>/', views.enroll_prime, name='enroll_prime'),
    path('wallet/', views.wallet_dashboard, name='wallet'),
    path('subscriptions/', views.subscriptions_dashboard, name='subscriptions'),
    path('subscriptions/toggle/<str:sub_id>/', views.toggle_subscription, name='toggle_subscription'),
]
