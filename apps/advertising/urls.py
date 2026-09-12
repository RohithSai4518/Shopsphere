from django.urls import path
from apps.advertising import views

app_name = 'advertising'

urlpatterns = [
    path('', views.AdvertisingDashboardView.as_view(), name='dashboard'),
    path('api/execute-second-price-vickrey-auction/', views.ExecuteSecondPriceVickreyAuctionApiView.as_view(), name='execute_second_price_vickrey_auction'),
    path('api/calculate-keyword-quality-score/', views.CalculateKeywordQualityScoreApiView.as_view(), name='calculate_keyword_quality_score'),
    path('api/resolve-ad-rank-score/', views.ResolveAdRankScoreApiView.as_view(), name='resolve_ad_rank_score'),
    path('api/match-search-query-to-keywords/', views.MatchSearchQueryToKeywordsApiView.as_view(), name='match_search_query_to_keywords'),
    path('api/pace-daily-advertising-budget/', views.PaceDailyAdvertisingBudgetApiView.as_view(), name='pace_daily_advertising_budget'),
    path('api/attribute-conversion-touchpoint/', views.AttributeConversionTouchpointApiView.as_view(), name='attribute_conversion_touchpoint'),
    path('api/detect-invalid-click-fraud/', views.DetectInvalidClickFraudApiView.as_view(), name='detect_invalid_click_fraud'),
    path('api/compute-campaign-roas-and-acos/', views.ComputeCampaignRoasAndAcosApiView.as_view(), name='compute_campaign_roas_and_acos'),
]

