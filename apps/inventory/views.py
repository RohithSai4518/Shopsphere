from django.http import HttpResponse

def inventory_status_view(request):
    return HttpResponse("Inventory Warehouse Ledger Engine Active")
