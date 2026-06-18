from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from academics.models import Student, Class, Attendance
from accounts.decorators import role_required
from .forms import StudentCreationForm
from accounts.models import User


# Create your views here.

@role_required('ADMIN', 'TEACHING_STAFF')
def students_list_per_class(request, class_id):
    _class = get_object_or_404(Class, id=class_id)
    students = _class.student_set.select_related('parent')

    context = {
        'students': students
    }

    return render(request, 'students/students_list_per_class.html', context)



@role_required('ADMIN', 'TEACHING_STAFF', 'PARENT')
def student_detail(request, student_id):
    student = get_object_or_404(Student.objects.select_related('parent', 'student_class'), student_id=student_id)
    if request.user.role == User.Roles.PARENT:
        if student.parent != request.user:
            raise PermissionDenied('You are not allowed here')  

    context = {
        'student': student
    }      

    return render(request, 'students/student_detail.html', context)
        


@login_required
@role_required('ADMIN')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentCreationForm(request.POST, instance=student)
        if form.is_valid():
            cache.delete('dashboard_summary')
            form.save()
            return redirect('academics:class', student.student_class.id )
    
    else:
        form = StudentCreationForm(instance=student)

    
    context = {
        'form' : form,
        'student': student
    }

    return render(request, 'students/edit_student.html', context)



@require_POST
@role_required('ADMIN', 'TEACHING_STAFF')
def mark_attendance(request):
    present_ids = request.POST.getlist('present_ids')
    class_id = request.POST.get('class_id')
    student_class = get_object_or_404(Class, id=class_id)
    students = Student.objects.filter(student_class=student_class)

    for student in students:
        Attendance.objects.update_or_create(
            student=student,
            date=timezone.now().date(),
            defaults={
                'is_present': str(student.id) in present_ids,
                'marked_by': request.user
            }
        )

    return JsonResponse({
        'success': True,
        'message': 'Attendance marked successfully'
    })



@role_required('ADMIN', 'TEACHING_STAFF')
def attendance_list(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        attendance = Attendance.objects.filter(
            
        )
    return render(request, 'students/attendance_list.html',)




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
    return render(request, 'students/add_student.html', context)




@require_POST
@login_required
@role_required('ADMIN')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    cache.delete('dashboard_summary')
    student.delete()

    return JsonResponse({
        'success': True,
        'message': 'Student deleted successfully'
    })


