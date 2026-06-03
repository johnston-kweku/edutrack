from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(*roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            request = args[0]
            if request.user.role not in roles:
                raise PermissionDenied('You are not allowed here')
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator
