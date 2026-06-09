from django.shortcuts import render
from accounts.decorators import role_required
# Create your views here.


@role_required('ADMIN')
def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')