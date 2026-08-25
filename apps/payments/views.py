from django.http import HttpResponse

def payment_status_view(request):
    return HttpResponse("Payment Sandbox Gateway Active")
