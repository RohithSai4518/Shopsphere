from django.urls import path
from apps.loyalty import views

app_name = 'loyalty'

urlpatterns = [
    path('', views.LoyaltyDashboardView.as_view(), name='dashboard'),
    path('api/calculate-earned-points-for-order/', views.CalculateEarnedPointsForOrderApiView.as_view(), name='calculate_earned_points_for_order'),
    path('api/evaluate-tier-promotion-status/', views.EvaluateTierPromotionStatusApiView.as_view(), name='evaluate_tier_promotion_status'),
    path('api/redeem-points-for-cart-discount/', views.RedeemPointsForCartDiscountApiView.as_view(), name='redeem_points_for_cart_discount'),
    path('api/unlock-eligible-gamification-badges/', views.UnlockEligibleGamificationBadgesApiView.as_view(), name='unlock_eligible_gamification_badges'),
    path('api/update-customer-milestone-streak/', views.UpdateCustomerMilestoneStreakApiView.as_view(), name='update_customer_milestone_streak'),
    path('api/calculate-point-expiration-schedule/', views.CalculatePointExpirationScheduleApiView.as_view(), name='calculate_point_expiration_schedule'),
    path('api/compute-customer-lifetime-reward-value/', views.ComputeCustomerLifetimeRewardValueApiView.as_view(), name='compute_customer_lifetime_reward_value'),
    path('api/generate-loyalty-account-statement/', views.GenerateLoyaltyAccountStatementApiView.as_view(), name='generate_loyalty_account_statement'),
]

