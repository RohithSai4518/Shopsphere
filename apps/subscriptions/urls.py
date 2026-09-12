from django.urls import path
from apps.subscriptions import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.SubscriptionsDashboardView.as_view(), name='dashboard'),
    path('api/calculate-next-delivery-date/', views.CalculateNextDeliveryDateApiView.as_view(), name='calculate_next_delivery_date'),
    path('api/compute-subscription-cadence-discount/', views.ComputeSubscriptionCadenceDiscountApiView.as_view(), name='compute_subscription_cadence_discount'),
    path('api/evaluate-customer-churn-risk/', views.EvaluateCustomerChurnRiskApiView.as_view(), name='evaluate_customer_churn_risk'),
    path('api/process-subscription-renewal-cycle/', views.ProcessSubscriptionRenewalCycleApiView.as_view(), name='process_subscription_renewal_cycle'),
    path('api/handle-failed-payment-retry-schedule/', views.HandleFailedPaymentRetryScheduleApiView.as_view(), name='handle_failed_payment_retry_schedule'),
    path('api/recommend-replenishment-frequency/', views.RecommendReplenishmentFrequencyApiView.as_view(), name='recommend_replenishment_frequency'),
    path('api/apply-bundle-subscription-savings/', views.ApplyBundleSubscriptionSavingsApiView.as_view(), name='apply_bundle_subscription_savings'),
    path('api/generate-subscription-cohort-metrics/', views.GenerateSubscriptionCohortMetricsApiView.as_view(), name='generate_subscription_cohort_metrics'),
]

