from django.contrib import admin
from apps.taxation.models import *

@admin.register(TaxJurisdiction)
class TaxJurisdictionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(NexusThreshold)
class NexusThresholdAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(TaxRateRule)
class TaxRateRuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(ProductTaxCode)
class ProductTaxCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(TaxExemptionCertificate)
class TaxExemptionCertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(TaxCalculationAudit)
class TaxCalculationAuditAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(HarmonizedSystemCode)
class HarmonizedSystemCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(VatOssFilingRecord)
class VatOssFilingRecordAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(EconomicNexusStateProfile)
class EconomicNexusStateProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(ImportTariffSchedule)
class ImportTariffScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

