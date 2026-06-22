from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
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
@role_required('ADMIN', 'TEACHING_STAFF')
def class_view(request, class_id): 

    query = request.GET.get('query', '')
    class_requested = get_object_or_404(Class.objects.select_related('class_teacher'),id=class_id)
    students = class_requested.student.all().select_related('parent')

    if query:
        students = students.filter(name__icontains=query)

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'class': class_requested,
        'page_obj': page_obj,
        'query': query
    }

    return render(request, 'academics/class.html', context)



@login_required
@role_required('ADMIN')
def teachers_view(request):
    teachers = User.objects.filter(role='TEACHING_STAFF').select_related('class_assigned')

    context = {
        'teachers': teachers
    }
    return render(request, 'academics/teachers.html', context)





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