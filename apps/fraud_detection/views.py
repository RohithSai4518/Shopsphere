from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.fraud_detection.models import *
from apps.fraud_detection.services import *

class FraudDetectionDashboardView(TemplateView):
    template_name = 'fraud_detection/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Real-Time Fraud Prevention & Risk Scoring Guard'
        context['record_count'] = FraudRule.objects.count()
        return context

class EvaluateOrderRiskScoreApiView(View):
    def get(self, request, *args, **kwargs):
        data = EvaluateOrderRiskScoreService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = EvaluateOrderRiskScoreService.execute(request.POST.dict())
        return JsonResponse(data)

class CheckCheckoutVelocityLimitsApiView(View):
    def get(self, request, *args, **kwargs):
        data = CheckCheckoutVelocityLimitsService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CheckCheckoutVelocityLimitsService.execute(request.POST.dict())
        return JsonResponse(data)

class DetectGeographicDistanceAnomalyApiView(View):
    def get(self, request, *args, **kwargs):
        data = DetectGeographicDistanceAnomalyService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = DetectGeographicDistanceAnomalyService.execute(request.POST.dict())
        return JsonResponse(data)

class InspectDeviceEntropyProfileApiView(View):
    def get(self, request, *args, **kwargs):
        data = InspectDeviceEntropyProfileService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = InspectDeviceEntropyProfileService.execute(request.POST.dict())
        return JsonResponse(data)

class TriageQuarantinedOrderCasesApiView(View):
    def get(self, request, *args, **kwargs):
        data = TriageQuarantinedOrderCasesService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = TriageQuarantinedOrderCasesService.execute(request.POST.dict())
        return JsonResponse(data)

class MatchBlacklistIdentifiersApiView(View):
    def get(self, request, *args, **kwargs):
        data = MatchBlacklistIdentifiersService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = MatchBlacklistIdentifiersService.execute(request.POST.dict())
        return JsonResponse(data)

class CalculateCustomerTrustScoreApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateCustomerTrustScoreService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateCustomerTrustScoreService.execute(request.POST.dict())
        return JsonResponse(data)

class GenerateRiskMitigationActionApiView(View):
    def get(self, request, *args, **kwargs):
        data = GenerateRiskMitigationActionService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = GenerateRiskMitigationActionService.execute(request.POST.dict())
        return JsonResponse(data)

