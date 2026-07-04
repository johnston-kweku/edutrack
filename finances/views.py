from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponse
from django.core.cache import cache
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from academics.models import Student, Term, Class
from .forms import FeeCreationForm, FeeRecordForm
from finances.models import Fee, FeePayment
from accounts.models import User
from accounts.decorators import role_required


@login_required
@role_required('ADMIN')
def dashboard_summary(request):
    cached_data = cache.get('dashboard_summary')
    if cached_data:
        print('Cache hit, returning immediately')
        return JsonResponse(cached_data)
    
    print('Cache miss, computing from memory')
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
            'student_name': payment.student.student_name,
            'student_class': str(payment.student.student_class),
            'amount': str(payment.amount_tendered),
            'status': status,
            'paid_at': payment.paid_at.strftime('%Y-%m-%d %H:%M'),
        })

    dashboard_data = {
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
    }

    cache.set(key='dashboard_summary', value=dashboard_data, timeout=300)

    return JsonResponse(dashboard_data)






@role_required('ADMIN')
def add_fee(request):
    if request.method == 'POST':
        form = FeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finances:add_fee')
    
    else:
        form = FeeCreationForm()
    
    context = {
        'form': form
    }

    return render(request, 'finances/add_fee.html', context)



@role_required('ADMIN')
def finances_view(request):
    return render(request, 'finances/finances.html')


@role_required('ADMIN')
def record_fee_payment(request):
    if request.method == 'POST':
        form = FeeRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finances:fee_payment')
        
    else:
        form = FeeRecordForm()
    
    context = {
        'form': form
    }

    return render(request, 'finances/record_fee_payment.html', context)




def get_students_by_fee(request):
    fee_id = request.GET.get('fee')
    options = '<option value="" disabled selected>Select student</option>'
    
    if fee_id:
        fee = get_object_or_404(Fee, pk=fee_id)
        students = Student.objects.filter(student_class=fee.student_class).order_by('student_name')
        for student in students:
            options += f'<option value="{student.pk}">{student.student_name} ({student.student_id})</option>'
    
    html = f'''
    <select name="student" id="id_student"
        class="block w-full pl-4 pr-10 py-2.5 border border-gray-200 rounded-xl bg-gray-50/50 text-gray-900 focus:outline-none focus:ring-2 focus:ring-amber-500/20 focus:border-amber-500 sm:text-sm appearance-none cursor-pointer">
        {options}
    </select>
    <div class="absolute inset-y-0 right-0 flex items-center px-3 pointer-events-none">
        <svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"/>
        </svg>
    </div>
    '''
    return HttpResponse(html)








from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta



@role_required('ADMIN')
def finances_view(request):
    # ===== Core Metrics =====
    total_fees = Fee.objects.count()

    # Total collected across all payments
    total_collected = FeePayment.objects.aggregate(
        total=Sum('amount_tendered')
    )['total'] or 0

    # Expected revenue = fee.amount × number of students in each class
    fees_with_student_counts = Fee.objects.annotate(
        student_count=Count('student_class__student', distinct=True)
    )
    total_expected = sum(
        f.amount * f.student_count for f in fees_with_student_counts
    )
    total_outstanding = total_expected - total_collected
    collection_rate = round((total_collected / total_expected * 100), 1) if total_expected > 0 else 0

    # Recent activity (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_payments_count = FeePayment.objects.filter(paid_at__gte=week_ago).count()
    recent_collected = FeePayment.objects.filter(paid_at__gte=week_ago).aggregate(
        total=Sum('amount_tendered')
    )['total'] or 0

    # ===== Recent Payments Table =====
    recent_payments = FeePayment.objects.select_related(
        'student', 'fee', 'fee__student_class', 'fee__term', 'received_by'
    ).order_by('-paid_at')[:10]

    # ===== Fees Overview Table =====
    fees = Fee.objects.select_related('term', 'student_class').annotate(
        total_paid=Sum('feepayment__amount_tendered'),
        payment_count=Count('feepayment'),
        student_count=Count('student_class__student', distinct=True)
    ).order_by('-term')[:10]

    # Calculate expected and completion % for each fee
    for fee in fees:
        fee.expected_amount = fee.amount * fee.student_count
        fee.collected_amount = fee.total_paid or 0
        fee.completion_rate = round(
            (fee.collected_amount / fee.expected_amount * 100), 1
        ) if fee.expected_amount > 0 else 0

    # ===== Outstanding Balances Table =====
    # Get latest payment per student-fee combo where balance > 0
    outstanding = FeePayment.objects.filter(
        balance__gt=0
    ).select_related(
        'student', 'fee', 'fee__student_class', 'fee__term'
    ).order_by('-balance')[:10]

    context = {
        # Stats
        'total_fees': total_fees,
        'total_expected': total_expected,
        'total_collected': total_collected,
        'total_outstanding': total_outstanding,
        'collection_rate': collection_rate,
        'recent_payments_count': recent_payments_count,
        'recent_collected': recent_collected,

        # Tables
        'recent_payments': recent_payments,
        'fees': fees,
        'outstanding': outstanding,
    }

    return render(request, 'finances/finances.html', context)