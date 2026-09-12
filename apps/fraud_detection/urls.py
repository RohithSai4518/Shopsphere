from django.urls import path
from apps.fraud_detection import views

app_name = 'fraud_detection'

urlpatterns = [
    path('', views.FraudDetectionDashboardView.as_view(), name='dashboard'),
    path('api/evaluate-order-risk-score/', views.EvaluateOrderRiskScoreApiView.as_view(), name='evaluate_order_risk_score'),
    path('api/check-checkout-velocity-limits/', views.CheckCheckoutVelocityLimitsApiView.as_view(), name='check_checkout_velocity_limits'),
    path('api/detect-geographic-distance-anomaly/', views.DetectGeographicDistanceAnomalyApiView.as_view(), name='detect_geographic_distance_anomaly'),
    path('api/inspect-device-entropy-profile/', views.InspectDeviceEntropyProfileApiView.as_view(), name='inspect_device_entropy_profile'),
    path('api/triage-quarantined-order-cases/', views.TriageQuarantinedOrderCasesApiView.as_view(), name='triage_quarantined_order_cases'),
    path('api/match-blacklist-identifiers/', views.MatchBlacklistIdentifiersApiView.as_view(), name='match_blacklist_identifiers'),
    path('api/calculate-customer-trust-score/', views.CalculateCustomerTrustScoreApiView.as_view(), name='calculate_customer_trust_score'),
    path('api/generate-risk-mitigation-action/', views.GenerateRiskMitigationActionApiView.as_view(), name='generate_risk_mitigation_action'),
]

