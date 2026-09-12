from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.advertising.models import *
from apps.advertising.services import *

class AdvertisingDashboardView(TemplateView):
    template_name = 'advertising/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Sponsored Products & PPC Auction Engine'
        context['record_count'] = AdCampaign.objects.count()
        return context

class ExecuteSecondPriceVickreyAuctionApiView(View):
    def get(self, request, *args, **kwargs):
        data = ExecuteSecondPriceVickreyAuctionService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ExecuteSecondPriceVickreyAuctionService.execute(request.POST.dict())
        return JsonResponse(data)

class CalculateKeywordQualityScoreApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateKeywordQualityScoreService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateKeywordQualityScoreService.execute(request.POST.dict())
        return JsonResponse(data)

class ResolveAdRankScoreApiView(View):
    def get(self, request, *args, **kwargs):
        data = ResolveAdRankScoreService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ResolveAdRankScoreService.execute(request.POST.dict())
        return JsonResponse(data)

class MatchSearchQueryToKeywordsApiView(View):
    def get(self, request, *args, **kwargs):
        data = MatchSearchQueryToKeywordsService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = MatchSearchQueryToKeywordsService.execute(request.POST.dict())
        return JsonResponse(data)

class PaceDailyAdvertisingBudgetApiView(View):
    def get(self, request, *args, **kwargs):
        data = PaceDailyAdvertisingBudgetService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = PaceDailyAdvertisingBudgetService.execute(request.POST.dict())
        return JsonResponse(data)

class AttributeConversionTouchpointApiView(View):
    def get(self, request, *args, **kwargs):
        data = AttributeConversionTouchpointService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = AttributeConversionTouchpointService.execute(request.POST.dict())
        return JsonResponse(data)

class DetectInvalidClickFraudApiView(View):
    def get(self, request, *args, **kwargs):
        data = DetectInvalidClickFraudService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = DetectInvalidClickFraudService.execute(request.POST.dict())
        return JsonResponse(data)

class ComputeCampaignRoasAndAcosApiView(View):
    def get(self, request, *args, **kwargs):
        data = ComputeCampaignRoasAndAcosService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ComputeCampaignRoasAndAcosService.execute(request.POST.dict())
        return JsonResponse(data)

