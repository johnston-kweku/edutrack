from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.cache import cache
from accounts.decorators import role_required
from .forms import StudentCreationForm, ClassCreationForm
from .models import Class, Student
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
@role_required('ADMIN')
def class_view(request, class_id): 
    class_requested = get_object_or_404(Class.objects.select_related('class_teacher').prefetch_related('student', 'student__parent'), id=class_id)

    context = {
        'class': class_requested
    }

    return render(request, 'academics/class.html', context)



@login_required
@role_required('ADMIN')
def teachers_view(request):
    pass



@login_required
@role_required('ADMIN')
def add_student(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            cache.delete('dashboard_summary')
            form.save()
            return redirect('academics:classes_list')
    else:
        form = StudentCreationForm()
    
    context = {
        'form': form
    }
    return render(request, 'academics/add_student.html', context)


@login_required
@role_required('ADMIN')
def delete_student(request, student_id):
    if request.method == 'POST':
        student = get_object_or_404(Student, student_id=student_id)
        cache.delete('dashboard_summary')
        student.delete()

        return JsonResponse({
            'success': True,
            'message': 'Student deleted successfully'
        })

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

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



