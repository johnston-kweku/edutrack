from django.contrib import admin
from .models import Class, Subject, ClassSubject, AcademicYear, Term, Student, Result, Attendance

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['level', 'stage', 'class_teacher']
    list_filter = ['level']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ['subject', 'subject_class', 'teacher']
    list_filter = ['subject_class']

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ['start_year', 'end_year', 'is_current']

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ['term', 'academic_year', 'is_current']
    list_filter = ['academic_year']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['student_id', 'name', 'student_class', 'gender', 'parent']
    list_filter = ['student_class', 'gender']
    search_fields = ['name', 'student_id']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'term', 'class_score', 'exam_score', 'total']
    list_filter = ['term', 'subject']
    search_fields = ['student__name']

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'date', 'is_present', 'marked_by']
    list_filter = ['date', 'is_present']
    search_fields = ['student__name']