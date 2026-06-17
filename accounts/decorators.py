from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from functools import wraps

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            
            if request.user.role not in roles:
                raise PermissionDenied('You are not allowed here')
            
            return func(request, *args, **kwargs)
        
        return wrapper
    return decorator
