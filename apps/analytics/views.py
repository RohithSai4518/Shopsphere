from django.http import HttpResponse

def analytics_overview_view(request):
    return HttpResponse("Analytics Service Active")
