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
@role_required('TEACHING_STAFF')
def teachers_dashboard(request):
    try:
        class_assigned = Class.objects.get(class_teacher=request.user)
    except Class.DoesNotExist:
        class_assigned = None

    if class_assigned:
        students = class_assigned.student.all().select_related('parent')
    return render(request, 'dashboards/teacher_dashboard.html')

@login_required
@role_required('PARENT')
def parents_dashboard(request):
    return render(request, 'dashboards/parents_dashboard.html')




