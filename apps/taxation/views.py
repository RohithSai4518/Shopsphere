from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.taxation.models import *
from apps.taxation.services import *

class TaxationDashboardView(TemplateView):
    template_name = 'taxation/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Global Multi-Jurisdiction Taxation & Customs Matrix'
        context['record_count'] = TaxJurisdiction.objects.count()
        return context

class CalculateSalesTaxForOrderApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateSalesTaxForOrderService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateSalesTaxForOrderService.execute(request.POST.dict())
        return JsonResponse(data)

class EvaluateEconomicNexusStatusApiView(View):
    def get(self, request, *args, **kwargs):
        data = EvaluateEconomicNexusStatusService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = EvaluateEconomicNexusStatusService.execute(request.POST.dict())
        return JsonResponse(data)

class ResolveHarmonizedTariffRateApiView(View):
    def get(self, request, *args, **kwargs):
        data = ResolveHarmonizedTariffRateService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ResolveHarmonizedTariffRateService.execute(request.POST.dict())
        return JsonResponse(data)

class ValidateExemptionCertificateApiView(View):
    def get(self, request, *args, **kwargs):
        data = ValidateExemptionCertificateService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ValidateExemptionCertificateService.execute(request.POST.dict())
        return JsonResponse(data)

class CalculateEuVatMossRateApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateEuVatMossRateService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateEuVatMossRateService.execute(request.POST.dict())
        return JsonResponse(data)

class ComputeCanadianGstPstSplitApiView(View):
    def get(self, request, *args, **kwargs):
        data = ComputeCanadianGstPstSplitService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ComputeCanadianGstPstSplitService.execute(request.POST.dict())
        return JsonResponse(data)

class AuditTaxCalculationDiscrepancyApiView(View):
    def get(self, request, *args, **kwargs):
        data = AuditTaxCalculationDiscrepancyService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = AuditTaxCalculationDiscrepancyService.execute(request.POST.dict())
        return JsonResponse(data)

class GenerateJurisdictionalTaxSummaryApiView(View):
    def get(self, request, *args, **kwargs):
        data = GenerateJurisdictionalTaxSummaryService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = GenerateJurisdictionalTaxSummaryService.execute(request.POST.dict())
        return JsonResponse(data)

