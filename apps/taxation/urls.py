from django.urls import path
from apps.taxation import views

app_name = 'taxation'

urlpatterns = [
    path('', views.TaxationDashboardView.as_view(), name='dashboard'),
    path('api/calculate-sales-tax-for-order/', views.CalculateSalesTaxForOrderApiView.as_view(), name='calculate_sales_tax_for_order'),
    path('api/evaluate-economic-nexus-status/', views.EvaluateEconomicNexusStatusApiView.as_view(), name='evaluate_economic_nexus_status'),
    path('api/resolve-harmonized-tariff-rate/', views.ResolveHarmonizedTariffRateApiView.as_view(), name='resolve_harmonized_tariff_rate'),
    path('api/validate-exemption-certificate/', views.ValidateExemptionCertificateApiView.as_view(), name='validate_exemption_certificate'),
    path('api/calculate-eu-vat-moss-rate/', views.CalculateEuVatMossRateApiView.as_view(), name='calculate_eu_vat_moss_rate'),
    path('api/compute-canadian-gst-pst-split/', views.ComputeCanadianGstPstSplitApiView.as_view(), name='compute_canadian_gst_pst_split'),
    path('api/audit-tax-calculation-discrepancy/', views.AuditTaxCalculationDiscrepancyApiView.as_view(), name='audit_tax_calculation_discrepancy'),
    path('api/generate-jurisdictional-tax-summary/', views.GenerateJurisdictionalTaxSummaryApiView.as_view(), name='generate_jurisdictional_tax_summary'),
]

