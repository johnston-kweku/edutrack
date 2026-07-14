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




def handle_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handle_500(request):
    return render(request, 'errors/500.html', status=500)

def handle_403(request, exception):
    return render(request, 'errors/403.html', status=403)