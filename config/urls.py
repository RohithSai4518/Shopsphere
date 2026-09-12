from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.catalog.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('cart/', include('apps.cart.urls')),
    path('wishlist/', include('apps.wishlist.urls')),
    path('orders/', include('apps.orders.urls')),
    path('payments/', include('apps.payments.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('seller/', include('apps.sellers.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('promotions/', include('apps.promotions.urls')),
    path('returns/', include('apps.returns.urls')),
    path('support/', include('apps.support.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('analytics/', include('apps.analytics.urls')),
    path('audit/', include('apps.audit.urls')),
    path('governance/', include('apps.administration.urls')),
    path('logistics/', include('apps.logistics.urls')),
    path('payouts/', include('apps.payouts.urls')),
    path('memberships/', include('apps.memberships.urls')),
    path('recommendations/', include('apps.recommendations.urls')),
    path('chat/', include('apps.chat.urls')),
    path('supply-chain/', include('apps.supply_chain.urls')),
    path('taxation/', include('apps.taxation.urls')),
    path('advertising/', include('apps.advertising.urls')),
    path('subscriptions/', include('apps.subscriptions.urls')),
    path('fraud-detection/', include('apps.fraud_detection.urls')),
    path('currency/', include('apps.currency.urls')),
    path('disputes/', include('apps.disputes.urls')),
    path('loyalty/', include('apps.loyalty.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'apps.catalog.views.error_404_view'
handler500 = 'apps.catalog.views.error_500_view'
handler403 = 'apps.catalog.views.error_403_view'

