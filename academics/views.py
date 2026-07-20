from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied, ValidationError
from django.db.models import Count, F, Case, When, BooleanField, Q
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from datetime import timedelta
import csv
from accounts.decorators import role_required
from .forms import ClassCreationForm, SubjectCreationForm, ClassSubjectCreationForm, TermForm, AcademicYearForm, AssessmentForm
from .models import Class, Subject, ClassSubject, Term, AcademicYear, Assessment, AssessmentRecord, Student
User = get_user_model()
# Create your views here.


@login_required
@role_required('ADMIN')
def classes_list(request):
    classes = Class.objects.all().select_related('class_teacher').annotate(students_count=Count('student', filter=Q(student__status='ENROLLED')))
    class_segregagtion = {
        'kindergarten': [],
        'lower_primary': [],
        'upper_primary': [],
        'JHS': []
    }
    for unchecked in classes:
        if unchecked.level == Class.Level.KINDERGARTEN:
            class_segregagtion['kindergarten'].append(unchecked)
        elif unchecked.level == Class.Level.LOWER_PRIMARY:
            class_segregagtion['lower_primary'].append(unchecked)
        elif unchecked.level == Class.Level.UPPER_PRIMARY:
            class_segregagtion['upper_primary'].append(unchecked)
        elif unchecked.level == Class.Level.JHS:
            class_segregagtion['JHS'].append(unchecked)

    classes_count = sum(len(v) for v in class_segregagtion.values())

    context = {
        'classes': class_segregagtion,
        'classes_count': classes_count,
    }
    return render(request, 'academics/classes_list.html', context)

@login_required
@role_required('ADMIN', 'TEACHING_STAFF')
def class_view(request, class_id):
    if request.user.is_teaching_staff():
        if not Class.objects.filter(id=class_id, class_teacher=request.user).exists():
            raise PermissionDenied("You do not have permission to view this class.")
    query = request.GET.get('query', '')
    status_filter = request.GET.get('status', Student.Status.ENROLLED)

    class_requested = get_object_or_404(
        Class.objects.select_related('class_teacher').annotate(
            students_count=Count('student', filter=Q(student__status='ENROLLED'))
        ),
        id=class_id
    )

    students = class_requested.student.all().select_related('parent')

    valid_statuses = {choice[0] for choice in Student.Status.choices}
    if status_filter in valid_statuses:
        students = students.filter(status=status_filter)
    # else: status_filter == 'ALL' (or anything unrecognized) → no filter applied

    if query:
        students = students.filter(student_name__icontains=query)

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'class': class_requested,
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'status_choices': Student.Status.choices,
    }

    return render(request, 'academics/class.html', context)





@role_required('ADMIN')
@login_required
def teachers_view(request):
    query = request.GET.get('query', '')
    status_filter = request.GET.get('status', '')

    
    teachers = User.objects.filter(role='TEACHING_STAFF')
    
    # Search
    if query:
        teachers = teachers.filter(full_name__icontains=query)
    
    # Filters
    if status_filter in ['true', 'false']:
        teachers = teachers.filter(is_active=(status_filter == 'true'))
    
    # Stats
    active_count = teachers.filter(is_active=True).count()
    classes_count = teachers.values('class_assigned').distinct().count()
    
    # Export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="teachers.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Title', 'Class', 'Contact', 'Email', 'Status'])
        for t in teachers:
            class_assigned = t.class_assigned if hasattr(t, 'class_assigned') else 'Not Assigned'
            writer.writerow([
                t.full_name, t.title, class_assigned,
                t.contact or '', t.email,
                'Active' if t.is_active else 'Inactive'
            ])
        return response
    
    paginator = Paginator(teachers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'active_count': active_count,
        'classes_count': classes_count,
        'status_filter': status_filter,
    }
    return render(request, 'academics/teachers.html', context)


@role_required('ADMIN')
@login_required
def parents_view(request):
    query = request.GET.get('query', '')
    has_student = request.GET.get('has_student', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    parents = User.objects.filter(role='PARENT').prefetch_related('student')
    
    # Search
    if query:
        parents = parents.filter(full_name__icontains=query)
    
    # Filters
    if has_student == 'yes':
        parents = parents.filter(student__isnull=False).distinct()
    elif has_student == 'no':
        parents = parents.filter(student__isnull=True)
    if date_from:
        parents = parents.filter(date_joined__date__gte=date_from)
    if date_to:
        parents = parents.filter(date_joined__date__lte=date_to)
    
    # Stats
    parents_count = parents.count()
    students_linked = parents.filter(student__isnull=False).count()
    new_parents_count = parents.filter(
        date_joined__gte=timezone.now() - timedelta(days=30)
    ).count()
    
    # Export
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="parents.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Contact', 'Student', 'Registered'])
        for p in parents:
            student = p.student.first()
            writer.writerow([
                p.full_name, p.email, p.contact or '',
                student.student_name if student else '—',
                p.date_joined.strftime('%Y-%m-%d') if p.date_joined else ''
            ])
        return response
    
    paginator = Paginator(parents, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'parents_count': parents_count,
        'students_linked': students_linked,
        'new_parents_count': new_parents_count,
        'has_student': has_student,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'academics/parents_list.html', context)



@login_required
@role_required('ADMIN')
def add_class(request):
    if request.method == 'POST':
        form = ClassCreationForm(request.POST)
        if form.is_valid():
            cache.delete('dashboard_summary')
            form.save()
            return redirect('academics:classes_list')

    else:
        form = ClassCreationForm()
    
    context = {
        'form': form
    }

    return render(request, 'academics/add_class.html', context)




@login_required
@role_required('ADMIN')
def edit_class(request, class_id):
    class_to_edit = get_object_or_404(Class, id=class_id)
    if request.method == 'POST':
        form = ClassCreationForm(request.POST, instance=class_to_edit)
        cache.delete('dashboard_summary')
        if form.is_valid():
            form.save()
            return redirect('academics:class', class_to_edit.id)

    else:
        form = ClassCreationForm(instance=class_to_edit)

    context = {
        'form': form,
        'class': class_to_edit
    }

    return render(request, 'academics/edit_class.html', context)





@role_required('ADMIN')
def academics_hub(request):
    subjects = Subject.objects.all()
    class_subjects = ClassSubject.objects.select_related('subject', 'subject_class', 'teacher').all()
    current_term = Term.objects.filter(is_current=True).select_related('academic_year').first()
    current_academic_year = AcademicYear.objects.filter(is_current=True).first()

    context = {
        'subjects': subjects,
        'class_subjects': class_subjects,
        'current_term': current_term,
        'current_academic_year': current_academic_year,
    }
    return render(request, 'academics/academics_hub.html', context)


@role_required('ADMIN')
def add_subject(request):
    if request.method == 'POST':
        form = SubjectCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('academics:add_subject')
        
    else:
        form = SubjectCreationForm()
    
    return render(request, 'academics/add_subject.html', {'form': form})


@role_required('ADMIN')
def add_class_subject(request):
    if request.method == 'POST':
        form = ClassSubjectCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Class subject added successfully.")
            return redirect('academics:add_class_subject')
        
    else:
        form = ClassSubjectCreationForm()
    
    return render(request, 'academics/add_class_subject.html', {'form': form})


@role_required('ADMIN')
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)

    if request.method == 'POST':
        form = SubjectCreationForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect('academics:academics_hub')
    else:
        form = SubjectCreationForm(instance=subject)

    return render(request, 'academics/edit_subject.html', {'form': form, 'subject': subject})


@role_required('ADMIN')
def edit_class_subject(request, class_subject_id):
    class_subject = get_object_or_404(ClassSubject, pk=class_subject_id)

    if request.method == 'POST':
        form = ClassSubjectCreationForm(request.POST, instance=class_subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Class subject updated successfully.")
            return redirect('academics:academics_hub')
    else:
        form = ClassSubjectCreationForm(instance=class_subject)

    return render(request, 'academics/edit_class_subject.html', {'form': form, 'class_subject': class_subject})
        



@role_required('ADMIN')
def add_academic_year(request):
    if request.method == 'POST':
        form = AcademicYearForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Academic year added successfully.")
            return redirect('academics:academics_hub')
    else:
        form = AcademicYearForm()
    return render(request, 'academics/academic_year_form.html', {'form': form, 'title': 'Add Academic Year'})


@role_required('ADMIN')
def edit_academic_year(request, pk):
    academic_year = get_object_or_404(AcademicYear, pk=pk)
    if request.method == 'POST':
        form = AcademicYearForm(request.POST, instance=academic_year)
        if form.is_valid():
            form.save()
            messages.success(request, "Academic year updated successfully.")
            return redirect('academics:academics_hub')
    else:
        form = AcademicYearForm(instance=academic_year)
    return render(request, 'academics/academic_year_form.html', {'form': form, 'title': 'Edit Academic Year'})


@role_required('ADMIN')
def add_term(request):
    if request.method == 'POST':
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Term added successfully.")
            return redirect('academics:academics_hub')
    else:
        form = TermForm()
    return render(request, 'academics/term_form.html', {'form': form, 'title': 'Add Term'})


@role_required('ADMIN')
def edit_term(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if request.method == 'POST':
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            messages.success(request, "Term updated successfully.")
            return redirect('academics:academics_hub')
    else:
        form = TermForm(instance=term)
    return render(request, 'academics/term_form.html', {'form': form, 'title': 'Edit Term'})




@role_required('TEACHING_STAFF')
def add_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST, user=request.user)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.recorded_by = request.user
            assessment.save()
            messages.success(request, "Assessment added successfully. You can continue to record marks right away")
            return redirect('academics:record_class_assessment', assessment_id=assessment.id)
    else:
        form = AssessmentForm(user=request.user)

    return render(request, 'academics/add_assessment.html', {'form': form})

@role_required('TEACHING_STAFF')
def edit_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id, recorded_by=request.user)

    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=assessment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Assessment updated successfully.")
            return redirect('academics:teacher_academics_hub')
    else:
        initial_class_subject = ClassSubject.objects.filter(
            subject=assessment.subject,
            subject_class=assessment.student_class,
        ).first()
        form = AssessmentForm(
            instance=assessment,
            user=request.user,
            initial={'class_subject': initial_class_subject}
        )

    return render(request, 'academics/edit_assessment.html', {'form': form, 'assessment': assessment})

@role_required('TEACHING_STAFF', 'ADMIN')
def record_class_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    class_subject_record = ClassSubject.objects.filter(
        subject_class=assessment.student_class,
        teacher=request.user,
        subject=assessment.subject
    )

    if not class_subject_record.exists():
        raise PermissionDenied("You do not have permission to record assessments for this class and subject.")

    if request.method == 'POST':
        student_id = int(request.POST.get('student_id'))

        try:
            score = Decimal(request.POST.get('score'))
        except (InvalidOperation, TypeError):
            return JsonResponse({'error': 'Invalid score value.'}, status=400)

        student = get_object_or_404(Student, id=student_id, student_class=assessment.student_class)

        try:
            AssessmentRecord.objects.update_or_create(
                assessment=assessment,
                student=student,
                defaults={'score': score}
            )
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({'message': 'Score recorded successfully.'})

    students = Student.objects.filter(student_class=assessment.student_class, status=Student.Status.ENROLLED).select_related('parent')
    existing_records = AssessmentRecord.objects.filter(assessment=assessment).values('student_id', 'score')
    existing_records_dict = {record['student_id']: record['score'] for record in existing_records}

    return render(request, 'academics/record_class_assessment.html', {
        'assessment': assessment,
        'students': students,
        'existing_records': existing_records_dict,
    })


@role_required('TEACHING_STAFF')
def teacher_academics_hub(request):
    teacher = request.user
    class_subjects = ClassSubject.objects.filter(teacher=teacher).select_related('subject', 'subject_class')
    try:
        class_assigned = Class.objects.get(class_teacher=teacher)
    except Class.DoesNotExist:
        class_assigned = None
    current_term = Term.objects.filter(is_current=True).select_related('academic_year').first()
    current_academic_year = AcademicYear.objects.filter(is_current=True).first()

    



    assessments = Assessment.objects.filter(
        recorded_by=request.user
    ).select_related('student_class', 'subject').annotate(
        recorded_count=Count('assessmentrecord', distinct=True),
        roster_size=Count(
            'student_class__student',
            filter=Q(student_class__student__status='ENROLLED'),
            distinct=True
        )
    ).annotate(
        is_incomplete=Case(
            When(recorded_count__lt=F('roster_size'), then=True),
            default=False,
            output_field=BooleanField()
        )
    ).order_by('-is_incomplete', '-date')

    context = {
        'class_subjects': class_subjects,
        'class_assigned': class_assigned,
        'current_term': current_term,   
        'current_academic_year': current_academic_year,
        'assessments': assessments,
    }
    return render(request, 'academics/teacher_academics_hub.html', context)


