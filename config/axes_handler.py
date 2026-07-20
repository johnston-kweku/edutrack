# accounts/axes_handlers.py

from django.http import JsonResponse


def axes_lockout_response(request, credentials, *args, **kwargs):
    from axes.helpers import get_cool_off

    cool_off = get_cool_off(request)  # returns a timedelta, or None if cooloff isn't set

    if cool_off:
        total_minutes = int(cool_off.total_seconds() // 60)
        if total_minutes >= 1:
            wait_message = f'Please try again in about {total_minutes} minute{"s" if total_minutes != 1 else ""}.'
        else:
            wait_message = 'Please try again shortly.'
    else:
        wait_message = 'Please try again later.'

    return JsonResponse({
        'success': False,
        'message': f'Too many failed attempts. {wait_message}'
    }, status=429)