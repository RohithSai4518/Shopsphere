from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.supply_chain.models import *
from apps.supply_chain.services import *

class SupplyChainDashboardView(TemplateView):
    template_name = 'supply_chain/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Supply Chain & Fulfillment Optimization'
        context['record_count'] = WarehouseFacility.objects.count()
        return context

class CalculateEconomicOrderQuantityApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateEconomicOrderQuantityService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateEconomicOrderQuantityService.execute(request.POST.dict())
        return JsonResponse(data)

class EstimateLeadTimeVarianceApiView(View):
    def get(self, request, *args, **kwargs):
        data = EstimateLeadTimeVarianceService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = EstimateLeadTimeVarianceService.execute(request.POST.dict())
        return JsonResponse(data)

class CalculateDynamicSafetyBufferApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateDynamicSafetyBufferService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateDynamicSafetyBufferService.execute(request.POST.dict())
        return JsonResponse(data)

class OptimizeCrossDockRoutingApiView(View):
    def get(self, request, *args, **kwargs):
        data = OptimizeCrossDockRoutingService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = OptimizeCrossDockRoutingService.execute(request.POST.dict())
        return JsonResponse(data)

class EvaluateVendorComplianceScoreApiView(View):
    def get(self, request, *args, **kwargs):
        data = EvaluateVendorComplianceScoreService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = EvaluateVendorComplianceScoreService.execute(request.POST.dict())
        return JsonResponse(data)

class ForecastInventoryDepletionVelocityApiView(View):
    def get(self, request, *args, **kwargs):
        data = ForecastInventoryDepletionVelocityService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ForecastInventoryDepletionVelocityService.execute(request.POST.dict())
        return JsonResponse(data)

class ComputePalletStackingDensityApiView(View):
    def get(self, request, *args, **kwargs):
        data = ComputePalletStackingDensityService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ComputePalletStackingDensityService.execute(request.POST.dict())
        return JsonResponse(data)

class GenerateInboundAsnManifestApiView(View):
    def get(self, request, *args, **kwargs):
        data = GenerateInboundAsnManifestService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = GenerateInboundAsnManifestService.execute(request.POST.dict())
        return JsonResponse(data)

