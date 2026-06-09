from django.shortcuts import render
from accounts.decorators import role_required
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


@role_required('ADMIN')
def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')