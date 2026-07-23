from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum
from decimal import Decimal
from academics.models import Class, Student, Term
from finances.models import Fee, FeePayment

from accounts.decorators import role_required
User = get_user_model()
# Create your views here.


def catch_all_404(request, *args, **kwargs):
    return render(request, 'errors/404.html', status=404)


@login_required
@role_required('ADMIN')
def admin_dashboard(request):
    return render(request, 'dashboards/admin_dashboard.html')


@login_required
@role_required('PARENT')
def parents_dashboard(request):
    parent = request.user
    wards = Student.objects.filter(
        parent=parent,
        status=Student.Status.ENROLLED
        ).select_related('student_class', 'student_class__class_teacher')
    current_term = Term.objects.get(is_current=True)

    total_fees_expected = Fee.objects.filter(
        term=current_term,
        student_class__student__in=wards
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
    
    total_fees_paid = FeePayment.objects.filter(
        fee__term=current_term,
        student__in=wards
        ).aggregate(total=Sum('amount_tendered'))['total'] or Decimal('0.00')
    
    outstanding_fees = round((total_fees_expected - total_fees_paid), 2)

    context = {
        'wards': wards,
        'total_fees_expected': total_fees_expected,
        'total_fees_paid': total_fees_paid,
        'outstanding_fees': outstanding_fees,
        'current_term': current_term
    }
    return render(request, 'dashboards/parents_dashboard.html', context)




def handle_404(request, exception):
    return render(request, 'errors/404.html', status=404)


def handle_500(request):
    return render(request, 'errors/500.html', status=500)

def handle_403(request, exception):
    return render(request, 'errors/403.html', status=403)