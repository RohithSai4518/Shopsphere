from django.urls import path
from apps.supply_chain import views

app_name = 'supply_chain'

urlpatterns = [
    path('', views.SupplyChainDashboardView.as_view(), name='dashboard'),
    path('api/calculate-economic-order-quantity/', views.CalculateEconomicOrderQuantityApiView.as_view(), name='calculate_economic_order_quantity'),
    path('api/estimate-lead-time-variance/', views.EstimateLeadTimeVarianceApiView.as_view(), name='estimate_lead_time_variance'),
    path('api/calculate-dynamic-safety-buffer/', views.CalculateDynamicSafetyBufferApiView.as_view(), name='calculate_dynamic_safety_buffer'),
    path('api/optimize-cross-dock-routing/', views.OptimizeCrossDockRoutingApiView.as_view(), name='optimize_cross_dock_routing'),
    path('api/evaluate-vendor-compliance-score/', views.EvaluateVendorComplianceScoreApiView.as_view(), name='evaluate_vendor_compliance_score'),
    path('api/forecast-inventory-depletion-velocity/', views.ForecastInventoryDepletionVelocityApiView.as_view(), name='forecast_inventory_depletion_velocity'),
    path('api/compute-pallet-stacking-density/', views.ComputePalletStackingDensityApiView.as_view(), name='compute_pallet_stacking_density'),
    path('api/generate-inbound-asn-manifest/', views.GenerateInboundAsnManifestApiView.as_view(), name='generate_inbound_asn_manifest'),
]

