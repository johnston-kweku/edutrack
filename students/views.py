from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from academics.models import Student, Class, Attendance, AttendanceRecord
from accounts.decorators import role_required
from .forms import StudentCreationForm
from accounts.models import User


# Create your views here.

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
        



@require_POST
@role_required('ADMIN', 'TEACHING_STAFF')
def mark_attendance(request, class_id):
    class_to_mark = get_object_or_404(Class, id=class_id)

    try:
        class_check = request.user.class_assigned
        if not request.user.is_admin() and class_to_mark != class_check:
            return JsonResponse({
            'success': False,
            'message': 'Cannot mark attendance for this class. Not assigned class'
        })    
    except Class.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'You have not been assigned a class. Please contact an administrator.'
        })    
    
    present_ids = request.POST.getlist('present_ids')

    attendance, _ = Attendance.objects.update_or_create(
        date=timezone.now().date(),
        class_marked=class_to_mark,
        defaults={'marked_by': request.user}
    )

    for student in class_to_mark.student.all():
        AttendanceRecord.objects.update_or_create(
            attendance=attendance,
            student=student,
            defaults={'is_present': str(student.id) in present_ids}
        )

    return JsonResponse({
        'success': True,
        'message': 'Class Attendance marked successfully'
    })


@role_required('ADMIN')
def attendance_list(request):
    classes = Class.objects.all()
    attendance = None
    attendance_records = []

    if request.method == 'POST':        
        class_id = request.POST.get('class_id')
        date = request.POST.get('date')

        if not class_id or not date:
            context = {
                'attendance': None,
                'attendance_records': [],
                'classes': classes,
                'error': 'Please select a class and date.'
            }
            return render(request, 'students/attendance_list.html', context)
        class_requested = get_object_or_404(Class, id=class_id)

        attendance = Attendance.objects.filter(
            date=date,
            class_marked=class_requested
        ).first()

    if attendance:
        attendance_records = AttendanceRecord.objects.filter(
            attendance=attendance
        ).select_related('student')

        present_count = attendance_records.filter(is_present=True).count()

    context = {
        'attendance': attendance,
        'attendance_records': attendance_records,
        'classes': classes,
        'present_count': present_count if attendance else None
    }
    return render(request, 'students/attendance_list.html', context)


@role_required('TEACHING_STAFF', 'ADMIN')
def mark_attendance_form(request):
    try:
        class_assigned = request.user.class_assigned
    except Class.DoesNotExist:
        class_assigned = None

    if class_assigned:
        attendance_today = Attendance.objects.filter(class_marked=class_assigned, date=timezone.now().date())
    

    context = {
        'class_assigned': class_assigned,
        'attendance_today': attendance_today if class_assigned else None

    }
    return render(request, 'students/mark_attendance.html', context)



@login_required
@role_required('ADMIN')
def add_student(request):
    if request.method == 'POST':
        form = StudentCreationForm(request.POST, request.FILES)
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


@login_required
@role_required('ADMIN')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentCreationForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            cache.delete('dashboard_summary')
            form.save()
            print(f'Files:{form.instance}')
            return redirect('academics:class', student.student_class.id )
    
    else:
        form = StudentCreationForm(instance=student)

    
    context = {
        'form' : form,
        'student': student
    }

    return render(request, 'students/edit_student.html', context)




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



def student_profile(request, student_id):
    student = get_object_or_404(Student.objects.select_related('parent', 'student_class'), id=student_id)
    context = {
        'student': student
    }
    return render(request, 'students/student_profile.html', context)
