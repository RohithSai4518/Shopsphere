from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import ShipmentParcel, WarehouseHub, Carrier, TrackingCheckpoint, DispatchManifest
from apps.orders.models import Order

def tracking_portal(request, tracking_number=None):
    parcel = None
    checkpoints = []
    searched = False
    
    if not tracking_number and request.method == 'GET':
        tracking_number = request.GET.get('tracking_number', '').strip()
        
    if tracking_number:
        searched = True
        try:
            parcel = ShipmentParcel.objects.select_related('carrier', 'hub', 'order').get(tracking_number__iexact=tracking_number)
            checkpoints = parcel.checkpoints.all()
        except ShipmentParcel.DoesNotExist:
            messages.error(request, f"Tracking number '{tracking_number}' could not be located in the ShopSphere fulfillment network.")

    return render(request, 'logistics/tracking_portal.html', {
        'parcel': parcel,
        'checkpoints': checkpoints,
        'tracking_number': tracking_number,
        'searched': searched
    })

def warehouse_dashboard(request, hub_id=None):
    hubs = WarehouseHub.objects.filter(is_active=True)
    current_hub = None
    parcels = []
    manifests = []
    
    if hub_id:
        current_hub = get_object_or_404(WarehouseHub, id=hub_id)
    elif hubs.exists():
        current_hub = hubs.first()
        
    if current_hub:
        parcels = ShipmentParcel.objects.filter(hub=current_hub).order_by('-created_at')[:25]
        manifests = DispatchManifest.objects.filter(hub=current_hub).order_by('-created_at')[:10]
        
    return render(request, 'logistics/warehouse_dashboard.html', {
        'hubs': hubs,
        'current_hub': current_hub,
        'parcels': parcels,
        'manifests': manifests
    })

def packing_slip(request, parcel_id):
    parcel = get_object_or_404(ShipmentParcel.objects.select_related('order', 'carrier', 'hub'), id=parcel_id)
    order_items = parcel.order.items.select_related('variant', 'variant__product', 'seller').all()
    return render(request, 'logistics/packing_slip.html', {
        'parcel': parcel,
        'order': parcel.order,
        'order_items': order_items
    })

def api_tracking_status(request, tracking_number):
    try:
        parcel = ShipmentParcel.objects.get(tracking_number__iexact=tracking_number)
        checkpoints = [{
            'milestone': cp.milestone_name,
            'facility': cp.facility_name,
            'location': f"{cp.city}, {cp.state}",
            'status': cp.status_code,
            'time': cp.recorded_at.isoformat(),
            'notes': cp.checkpoint_notes
        } for cp in parcel.checkpoints.all()]
        return JsonResponse({
            'status': 'success',
            'tracking_number': parcel.tracking_number,
            'carrier': parcel.carrier.name,
            'parcel_status': parcel.status,
            'current_location': parcel.current_location_desc,
            'estimated_delivery': parcel.estimated_delivery.isoformat() if parcel.estimated_delivery else None,
            'checkpoints': checkpoints
        })
    except ShipmentParcel.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Tracking number not found'}, status=404)
