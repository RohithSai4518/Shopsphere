from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Auth & Sessions
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('two-factor/verify/', views.two_factor_verify_view, name='two_factor_verify'),
    path('two-factor/setup/', views.two_factor_setup_view, name='two_factor_setup'),
    path('2fa/setup/', views.two_factor_setup_view, name='two_factor_setup_alias'),
    path('2fa/verify/', views.two_factor_verify_view, name='two_factor_verify_alias'),

    # Self-Service Password Reset
    path('password_reset/', views.password_reset_request_view, name='password_reset_request'),
    path('password_reset/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),

    # User Profile & Address Book
    path('profile/', views.profile_view, name='profile'),
    path('address/add/', views.add_address_view, name='add_address'),
    path('address/<str:address_id>/delete/', views.delete_address_view, name='delete_address'),

    # Payment Methods Vault
    path('payment-methods/', views.payment_methods_view, name='payment_methods'),
    path('payment-methods/<str:payment_id>/delete/', views.delete_payment_method_view, name='delete_payment_method'),
    path('payment-methods/<str:payment_id>/default/', views.set_default_payment_method_view, name='set_default_payment_method'),

    # GDPR Privacy & Data Subject Rights
    path('privacy/', views.privacy_dashboard_view, name='privacy'),
    path('privacy/export/', views.export_user_data_view, name='export_user_data'),
    path('privacy/delete-account/', views.request_account_deletion_view, name='delete_account'),
]
