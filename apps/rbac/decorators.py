from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.shortcuts import redirect

def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please log in to access this page.')
                return redirect('accounts:login')
            if request.user.role in roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            messages.error(request, 'Access Denied: You do not have permission to view this resource.')
            return redirect('/')
        return _wrapped_view
    return decorator
