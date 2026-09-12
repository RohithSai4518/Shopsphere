from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.disputes.models import *
from apps.disputes.services import *

class DisputesDashboardView(TemplateView):
    template_name = 'disputes/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Buyer-Seller Dispute Arbitration Tribunal'
        context['record_count'] = DisputeClaim.objects.count()
        return context

class InitiateDisputeClaimWorkflowApiView(View):
    def get(self, request, *args, **kwargs):
        data = InitiateDisputeClaimWorkflowService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = InitiateDisputeClaimWorkflowService.execute(request.POST.dict())
        return JsonResponse(data)

class ValidateEvidenceSubmissionApiView(View):
    def get(self, request, *args, **kwargs):
        data = ValidateEvidenceSubmissionService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ValidateEvidenceSubmissionService.execute(request.POST.dict())
        return JsonResponse(data)

class FreezeEscrowDisputeFundsApiView(View):
    def get(self, request, *args, **kwargs):
        data = FreezeEscrowDisputeFundsService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = FreezeEscrowDisputeFundsService.execute(request.POST.dict())
        return JsonResponse(data)

class AdjudicateTribunalRulingApiView(View):
    def get(self, request, *args, **kwargs):
        data = AdjudicateTribunalRulingService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = AdjudicateTribunalRulingService.execute(request.POST.dict())
        return JsonResponse(data)

class CalculateMerchantDefectRateApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateMerchantDefectRateService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateMerchantDefectRateService.execute(request.POST.dict())
        return JsonResponse(data)

class ProcessAppealEscalationApiView(View):
    def get(self, request, *args, **kwargs):
        data = ProcessAppealEscalationService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ProcessAppealEscalationService.execute(request.POST.dict())
        return JsonResponse(data)

class ReleaseDisputeEscrowSettlementApiView(View):
    def get(self, request, *args, **kwargs):
        data = ReleaseDisputeEscrowSettlementService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ReleaseDisputeEscrowSettlementService.execute(request.POST.dict())
        return JsonResponse(data)

class GenerateArbitrationSummaryTranscriptApiView(View):
    def get(self, request, *args, **kwargs):
        data = GenerateArbitrationSummaryTranscriptService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = GenerateArbitrationSummaryTranscriptService.execute(request.POST.dict())
        return JsonResponse(data)

