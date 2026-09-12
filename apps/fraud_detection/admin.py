from django.contrib import admin
from apps.fraud_detection.models import *

@admin.register(FraudRule)
class FraudRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(CheckoutRiskScore)
class CheckoutRiskScoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(VelocityCounter)
class VelocityCounterAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(BlacklistedIdentifier)
class BlacklistedIdentifierAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(QuarantinedOrder)
class QuarantinedOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(FraudInvestigationCase)
class FraudInvestigationCaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(DeviceFingerprintProfile)
class DeviceFingerprintProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(GeographicAnomalyLog)
class GeographicAnomalyLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(ChargebackRiskIndex)
class ChargebackRiskIndexAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(TrustFactorCredential)
class TrustFactorCredentialAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

