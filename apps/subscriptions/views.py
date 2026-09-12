from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.subscriptions.models import *
from apps.subscriptions.services import *

class SubscriptionsDashboardView(TemplateView):
    template_name = 'subscriptions/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Subscribe & Save Auto-Replenishment Commerce'
        context['record_count'] = SubscriptionPlan.objects.count()
        return context

class CalculateNextDeliveryDateApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateNextDeliveryDateService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateNextDeliveryDateService.execute(request.POST.dict())
        return JsonResponse(data)

class ComputeSubscriptionCadenceDiscountApiView(View):
    def get(self, request, *args, **kwargs):
        data = ComputeSubscriptionCadenceDiscountService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ComputeSubscriptionCadenceDiscountService.execute(request.POST.dict())
        return JsonResponse(data)

class EvaluateCustomerChurnRiskApiView(View):
    def get(self, request, *args, **kwargs):
        data = EvaluateCustomerChurnRiskService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = EvaluateCustomerChurnRiskService.execute(request.POST.dict())
        return JsonResponse(data)

class ProcessSubscriptionRenewalCycleApiView(View):
    def get(self, request, *args, **kwargs):
        data = ProcessSubscriptionRenewalCycleService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ProcessSubscriptionRenewalCycleService.execute(request.POST.dict())
        return JsonResponse(data)

class HandleFailedPaymentRetryScheduleApiView(View):
    def get(self, request, *args, **kwargs):
        data = HandleFailedPaymentRetryScheduleService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = HandleFailedPaymentRetryScheduleService.execute(request.POST.dict())
        return JsonResponse(data)

class RecommendReplenishmentFrequencyApiView(View):
    def get(self, request, *args, **kwargs):
        data = RecommendReplenishmentFrequencyService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = RecommendReplenishmentFrequencyService.execute(request.POST.dict())
        return JsonResponse(data)

class ApplyBundleSubscriptionSavingsApiView(View):
    def get(self, request, *args, **kwargs):
        data = ApplyBundleSubscriptionSavingsService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ApplyBundleSubscriptionSavingsService.execute(request.POST.dict())
        return JsonResponse(data)

class GenerateSubscriptionCohortMetricsApiView(View):
    def get(self, request, *args, **kwargs):
        data = GenerateSubscriptionCohortMetricsService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = GenerateSubscriptionCohortMetricsService.execute(request.POST.dict())
        return JsonResponse(data)

