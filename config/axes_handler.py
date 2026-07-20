from django.http import JsonResponse

def axes_lockout_response(request, credentials, *args, **kwargs):
    return JsonResponse({
        'success': False,
        'message': 'Too many failed attempts. Please try again later.'
    }, status=429)