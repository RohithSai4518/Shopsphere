from django.urls import path
from apps.disputes import views

app_name = 'disputes'

urlpatterns = [
    path('', views.DisputesDashboardView.as_view(), name='dashboard'),
    path('api/initiate-dispute-claim-workflow/', views.InitiateDisputeClaimWorkflowApiView.as_view(), name='initiate_dispute_claim_workflow'),
    path('api/validate-evidence-submission/', views.ValidateEvidenceSubmissionApiView.as_view(), name='validate_evidence_submission'),
    path('api/freeze-escrow-dispute-funds/', views.FreezeEscrowDisputeFundsApiView.as_view(), name='freeze_escrow_dispute_funds'),
    path('api/adjudicate-tribunal-ruling/', views.AdjudicateTribunalRulingApiView.as_view(), name='adjudicate_tribunal_ruling'),
    path('api/calculate-merchant-defect-rate/', views.CalculateMerchantDefectRateApiView.as_view(), name='calculate_merchant_defect_rate'),
    path('api/process-appeal-escalation/', views.ProcessAppealEscalationApiView.as_view(), name='process_appeal_escalation'),
    path('api/release-dispute-escrow-settlement/', views.ReleaseDisputeEscrowSettlementApiView.as_view(), name='release_dispute_escrow_settlement'),
    path('api/generate-arbitration-summary-transcript/', views.GenerateArbitrationSummaryTranscriptApiView.as_view(), name='generate_arbitration_summary_transcript'),
]

