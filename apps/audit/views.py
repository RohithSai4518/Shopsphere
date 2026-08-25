from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.rbac.decorators import role_required
from .models import SecurityAuditLog

@login_required
@role_required('ADMIN')
def audit_log_list_view(request):
    logs = SecurityAuditLog.objects.all()[:50]
    return render(request, 'audit/log_list.html', {'logs': logs})
