from django.shortcuts import render
from accounts.decorators import role_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.


@login_required
@role_required('ADMIN')
def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')

@login_required
@role_required('TEACHING_STAFF', 'ADMIN')
def teachers_dashboard(request):
    return render(request, 'dashboards/teacher_dashboard.html')

@login_required
@role_required('PARENT')
def parents_dashboard(request):
    return render(request, 'dashboards/parents_dashboard.html')




