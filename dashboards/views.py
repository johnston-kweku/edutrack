from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from academics.models import Class, Student
from accounts.decorators import role_required
User = get_user_model()
# Create your views here.


@login_required
@role_required('ADMIN')
def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')


@login_required
@role_required('PARENT')
def parents_dashboard(request):
    return render(request, 'dashboards/parents_dashboard.html')




