from django.urls import path
from apps.currency import views

app_name = 'currency'

urlpatterns = [
    path('', views.CurrencyDashboardView.as_view(), name='dashboard'),
    path('api/convert-currency-amount/', views.ConvertCurrencyAmountApiView.as_view(), name='convert_currency_amount'),
    path('api/apply-charm-pricing-rounding/', views.ApplyCharmPricingRoundingApiView.as_view(), name='apply_charm_pricing_rounding'),
    path('api/synchronize-daily-fx-rates/', views.SynchronizeDailyFxRatesApiView.as_view(), name='synchronize_daily_fx_rates'),
    path('api/calculate-cross-border-conversion-fee/', views.CalculateCrossBorderConversionFeeApiView.as_view(), name='calculate_cross_border_conversion_fee'),
    path('api/estimate-currency-hedging-reserve/', views.EstimateCurrencyHedgingReserveApiView.as_view(), name='estimate_currency_hedging_reserve'),
    path('api/format-localized-currency-display/', views.FormatLocalizedCurrencyDisplayApiView.as_view(), name='format_localized_currency_display'),
    path('api/reconcile-merchant-payout-currency/', views.ReconcileMerchantPayoutCurrencyApiView.as_view(), name='reconcile_merchant_payout_currency'),
    path('api/compute-fx-volatility-risk-spread/', views.ComputeFxVolatilityRiskSpreadApiView.as_view(), name='compute_fx_volatility_risk_spread'),
]

