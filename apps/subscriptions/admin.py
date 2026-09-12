from django.contrib import admin
from apps.subscriptions.models import *

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(CustomerSubscription)
class CustomerSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(SubscriptionItem)
class SubscriptionItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(DeliverySchedule)
class DeliveryScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(RenewalRetryLog)
class RenewalRetryLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(ChurnPredictionScore)
class ChurnPredictionScoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(SubscriptionSkipEvent)
class SubscriptionSkipEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(CadenceDiscountTier)
class CadenceDiscountTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(ReplenishmentTriggerRule)
class ReplenishmentTriggerRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(SubscriptionLifecycleAudit)
class SubscriptionLifecycleAuditAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

