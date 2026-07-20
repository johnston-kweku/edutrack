# accounts/helpers.py (or wherever your account-related helpers live)

from django.urls import reverse


def get_dashboard_url_for_user(user):
    """
    Single source of truth for role -> dashboard routing.
    Used both for the 'already logged in' redirect and post-login redirect,
    so a new role only ever needs to be added here once.
    """
    if user.is_admin():
        return reverse('dashboards:admin_dashboard')
    elif user.is_teaching_staff():
        return reverse('academics:teacher_academics_hub')
    elif user.is_parent():
        return reverse('dashboards:parents_dashboard')
    # Deliberately explicit fallback — a role that matches none of the above
    # should never silently fall through and leave a view returning None.
    return reverse('accounts:login')