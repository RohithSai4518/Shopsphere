from django.contrib import admin
from apps.currency.models import *

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(HistoricalFXRate)
class HistoricalFXRateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(CurrencyRoundingRule)
class CurrencyRoundingRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(MerchantSettlementPreference)
class MerchantSettlementPreferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(CurrencyHedgeReserve)
class CurrencyHedgeReserveAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(FxVolatilityIndex)
class FxVolatilityIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(MultiCurrencyPriceCache)
class MultiCurrencyPriceCacheAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(CrossBorderFeeSchedule)
class CrossBorderFeeScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(CurrencyConversionAudit)
class CurrencyConversionAuditAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

