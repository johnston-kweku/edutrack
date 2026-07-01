from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta
import csv
from accounts.decorators import role_required
from .forms import ClassCreationForm
from .models import Class
User = get_user_model()
# Create your views here.


@login_required
@role_required('ADMIN')
def classes_list(request):
    classes = Class.objects.all().select_related('class_teacher').annotate(students_count=Count('student'))
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

    query = request.GET.get('query', '')
    class_requested = get_object_or_404(Class.objects.select_related('class_teacher'),id=class_id)
    students = class_requested.student.all().select_related('parent')

    if query:
        students = students.filter(student_name__icontains=query)

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'class': class_requested,
        'page_obj': page_obj,
        'query': query
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