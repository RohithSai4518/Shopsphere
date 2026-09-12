from django.contrib import admin
from apps.supply_chain.models import *

@admin.register(WarehouseFacility)
class WarehouseFacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(FreightCarrier)
class FreightCarrierAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(ReplenishmentOrder)
class ReplenishmentOrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(SafetyStockPolicy)
class SafetyStockPolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(CrossDockRouting)
class CrossDockRoutingAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(VendorScorecard)
class VendorScorecardAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(InboundShipmentManifest)
class InboundShipmentManifestAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(DistributionHubRoute)
class DistributionHubRouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

@admin.register(InventorySafetyThreshold)
class InventorySafetyThresholdAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'status', 'priority', 'metric_score', 'created_at')
    list_filter = ('status', 'priority', 'is_active')
    search_fields = ('name', 'code', 'description')

