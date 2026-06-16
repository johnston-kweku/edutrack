from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import get_user_model
from accounts.decorators import role_required
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

    classes_count = classes.count()

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
    teachers = User.objects.filter(role='TEACHING_STAFF')