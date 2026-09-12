from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.loyalty.models import *
from apps.loyalty.services import *

class LoyaltyDashboardView(TemplateView):
    template_name = 'loyalty/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['module_name'] = 'Tiered Customer Loyalty & Gamification Rewards'
        context['record_count'] = LoyaltyTier.objects.count()
        return context

class CalculateEarnedPointsForOrderApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculateEarnedPointsForOrderService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculateEarnedPointsForOrderService.execute(request.POST.dict())
        return JsonResponse(data)

class EvaluateTierPromotionStatusApiView(View):
    def get(self, request, *args, **kwargs):
        data = EvaluateTierPromotionStatusService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = EvaluateTierPromotionStatusService.execute(request.POST.dict())
        return JsonResponse(data)

class RedeemPointsForCartDiscountApiView(View):
    def get(self, request, *args, **kwargs):
        data = RedeemPointsForCartDiscountService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = RedeemPointsForCartDiscountService.execute(request.POST.dict())
        return JsonResponse(data)

class UnlockEligibleGamificationBadgesApiView(View):
    def get(self, request, *args, **kwargs):
        data = UnlockEligibleGamificationBadgesService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = UnlockEligibleGamificationBadgesService.execute(request.POST.dict())
        return JsonResponse(data)

class UpdateCustomerMilestoneStreakApiView(View):
    def get(self, request, *args, **kwargs):
        data = UpdateCustomerMilestoneStreakService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = UpdateCustomerMilestoneStreakService.execute(request.POST.dict())
        return JsonResponse(data)

class CalculatePointExpirationScheduleApiView(View):
    def get(self, request, *args, **kwargs):
        data = CalculatePointExpirationScheduleService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = CalculatePointExpirationScheduleService.execute(request.POST.dict())
        return JsonResponse(data)

class ComputeCustomerLifetimeRewardValueApiView(View):
    def get(self, request, *args, **kwargs):
        data = ComputeCustomerLifetimeRewardValueService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = ComputeCustomerLifetimeRewardValueService.execute(request.POST.dict())
        return JsonResponse(data)

class GenerateLoyaltyAccountStatementApiView(View):
    def get(self, request, *args, **kwargs):
        data = GenerateLoyaltyAccountStatementService.execute()
        return JsonResponse(data)

    def post(self, request, *args, **kwargs):
        data = GenerateLoyaltyAccountStatementService.execute(request.POST.dict())
        return JsonResponse(data)

