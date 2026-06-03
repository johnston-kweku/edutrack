from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.dateparse import parse_date
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

@role_required('ADMIN', 'TEACHING_STAFF')
def enroll_student(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True, 
                'message': 'Student added succesfully'
            })
        
        return JsonResponse({
            'success': False,
            'message': f'{form.errors}'
        })
    
    render(request, 'students/enroll.html')


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
        
    
@role_required('ADMIN')
def edit_student(request, student_id):
    student = get_object_or_404(Student,  student_id=student_id)
    if request.method == 'POST':
        form = StudentCreationForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': True, 
                'message': 'Student added succesfully'
            })
        
        return JsonResponse({
            'success': False,
            'message': f'{form.errors}'
        })
    
    else:
        form = StudentCreationForm(instance=student)

    
    return render(request, 'student/edit_student.html')

@require_POST
@role_required('ADMIN')
def delete_student(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    student.delete()
    return JsonResponse({
        'success': True,
        'message': 'Student deleted successfully'
    })


@require_POST
@role_required('ADMIN', 'TEACHING_STAFF')
def mark_attendace(request):
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
        'message': 'Attendace marked successflly'
    })



@role_required('ADMIN', 'TEACHING_STAFF')
def attendance_list(request):
    class_id = request.GET.get('class_id')
    students_class = get_object_or_404(Class, id=class_id)
    date = request.GET.get('date')
    attendance = Attendance.objects.filter(
        student__student_class=students_class,
        date=parse_date(date)
    )


    context = {'attendance': [
            {
                'student': record.student.name,
                'is_present': record.is_present
            }
            for record in attendance
        ]
    }

    return render(request, 'students/attendance_list.html', context)