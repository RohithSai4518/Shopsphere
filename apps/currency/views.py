from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.currency.models import *
from apps.currency.services import *

class CurrencyDashboardView(TemplateView):
    template_name = 'currency/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Multi-Currency Settlement & Real-Time FX Matrix'
        context['record_count'] = Currency.objects.count()
        return context

class ConvertCurrencyAmountApiView(View):
    def get(self, request, *args, **kwargs):
        data = ConvertCurrencyAmountService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ConvertCurrencyAmountService.execute(request.POST.dict())
        return JsonResponse(data)

class ApplyCharmPricingRoundingApiView(View):
    def get(self, request, *args, **kwargs):
        data = ApplyCharmPricingRoundingService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ApplyCharmPricingRoundingService.execute(request.POST.dict())
        return JsonResponse(data)

class SynchronizeDailyFxRatesApiView(View):
    def get(self, request, *args, **kwargs):
        data = SynchronizeDailyFxRatesService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = SynchronizeDailyFxRatesService.execute(request.POST.dict())
        return JsonResponse(data)

class CalculateCrossBorderConversionFeeApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateCrossBorderConversionFeeService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateCrossBorderConversionFeeService.execute(request.POST.dict())
        return JsonResponse(data)

class EstimateCurrencyHedgingReserveApiView(View):
    def get(self, request, *args, **kwargs):
        data = EstimateCurrencyHedgingReserveService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = EstimateCurrencyHedgingReserveService.execute(request.POST.dict())
        return JsonResponse(data)

class FormatLocalizedCurrencyDisplayApiView(View):
    def get(self, request, *args, **kwargs):
        data = FormatLocalizedCurrencyDisplayService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = FormatLocalizedCurrencyDisplayService.execute(request.POST.dict())
        return JsonResponse(data)

class ReconcileMerchantPayoutCurrencyApiView(View):
    def get(self, request, *args, **kwargs):
        data = ReconcileMerchantPayoutCurrencyService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ReconcileMerchantPayoutCurrencyService.execute(request.POST.dict())
        return JsonResponse(data)

class ComputeFxVolatilityRiskSpreadApiView(View):
    def get(self, request, *args, **kwargs):
        data = ComputeFxVolatilityRiskSpreadService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ComputeFxVolatilityRiskSpreadService.execute(request.POST.dict())
        return JsonResponse(data)

