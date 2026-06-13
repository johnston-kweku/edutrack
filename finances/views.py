from decimal import Decimal
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from academics.models import Student, Term, Class
from finances.models import Fee, FeePayment
from accounts.models import User
from accounts.decorators import role_required


@login_required
@role_required('ADMIN')
def dashboard_summary(request):
    try:
        current_term = Term.objects.select_related('academic_year').get(is_current=True)
    except Term.DoesNotExist:
        return JsonResponse({'error': 'No active term set.'}, status=400)

    academic_year = current_term.academic_year

    total_students = Student.objects.count()
    total_teachers = User.objects.filter(role='TEACHING_STAFF').count()
    total_classes = Class.objects.count()

    fees_this_term = Fee.objects.filter(
        term=current_term
    ).select_related('student_class').annotate(
        student_count=Count('student_class__student')
    )

    total_expected = sum(
        fee.amount * fee.student_count for fee in fees_this_term
    )
    total_expected = total_expected or Decimal('0.00')

    total_collected = FeePayment.objects.filter(
        fee__term=current_term
    ).aggregate(total=Sum('amount_tendered'))['total'] or Decimal('0.00')

    total_outstanding = total_expected - total_collected

    collection_percentage = round(
        (total_collected / total_expected * 100), 1
    ) if total_expected > 0 else 0

    student_payment_summary = FeePayment.objects.filter(
        fee__term=current_term
    ).values('student', 'fee__amount').annotate(
        total_paid=Sum('amount_tendered')
    )

    fully_paid_count = 0
    partially_paid_count = 0
    partially_paid_amount = Decimal('0.00')
    students_with_payments = set()

    for entry in student_payment_summary:
        students_with_payments.add(entry['student'])
        fee_amount = entry['fee__amount']
        total_paid = entry['total_paid'] or Decimal('0.00')

        if total_paid >= fee_amount:
            fully_paid_count += 1
        else:
            partially_paid_count += 1
            partially_paid_amount += fee_amount - total_paid

    outstanding_count = total_students - len(students_with_payments)

    recent_payments = FeePayment.objects.filter(
        fee__term=current_term
    ).select_related(
        'student', 'student__student_class', 'fee'
    ).order_by('-paid_at')[:5]

    student_ids = [p.student_id for p in recent_payments]
    totals_map = {
        entry['student']: entry['total_paid']
        for entry in FeePayment.objects.filter(
            fee__term=current_term,
            student_id__in=student_ids
        ).values('student').annotate(total_paid=Sum('amount_tendered'))
    }

    transactions = []
    for payment in recent_payments:
        total_paid = totals_map.get(payment.student_id, Decimal('0.00'))
        status = 'Paid' if total_paid >= payment.fee.amount else 'Partial'
        transactions.append({
            'student_name': payment.student.name,
            'student_class': str(payment.student.student_class),
            'amount': str(payment.amount_tendered),
            'status': status,
            'paid_at': payment.paid_at.strftime('%Y-%m-%d %H:%M'),
        })

    return JsonResponse({
        'current_term': current_term.term,
        'academic_year': str(academic_year),
        'stats': {
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_classes': total_classes,
            'fees_collected': str(total_collected),
        },
        'fee_status': {
            'expected': str(total_expected),
            'collected': str(total_collected),
            'outstanding_amount': str(total_outstanding),
            'collection_percentage': collection_percentage,
            'fully_paid_count': fully_paid_count,
            'partially_paid_amount': str(partially_paid_amount),
            'partially_paid_count': partially_paid_count,
            'outstanding_count': outstanding_count,
        },
        'recent_transactions': transactions,
    })