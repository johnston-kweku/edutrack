from django.contrib import admin
from .models import Class, Subject, ClassSubject, AcademicYear, Term, Student, Assessment, AssessmentRecord, Attendance, AttendanceRecord

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


class AssessmentRecordInline(admin.TabularInline):
    model = AssessmentRecord
    extra = 0
    fields = ('student', 'score')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        # 'obj' is the parent Assessment instance being edited
        if obj and obj.student_class:
            # Filter the student queryset dynamically to only match this subject's class
            # Adjust 'student_class' to match the actual ForeignKey field name on your Student model
            formset.form.base_fields['student'].queryset = formset.form.base_fields['student'].queryset.filter(
                student_class=obj.student_class
            )
        else:
            # If it's a brand new assessment and no subject is selected yet,
            # show an empty queryset so the admin doesn't load thousands of irrelevant students.
            formset.form.base_fields['student'].queryset = formset.form.base_fields['student'].queryset.none()
            
        return formset
    
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['assessment_type', 'subject', 'term', 'academic_year', 'recorded_by']
    list_filter = ['assessment_type', 'subject', 'term', 'academic_year']
    inlines = [AssessmentRecordInline]




class AttendanceRecordInline(admin.TabularInline):
    model = AttendanceRecord
    extra = 0
    fields = ('student', 'is_present')

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        
        # 'obj' is the parent Attendance instance being edited
        if obj and obj.class_marked:
            # Filter the student queryset dynamically to only match this class
            # Adjust 'student_class' to match the actual ForeignKey field name on your Student model
            formset.form.base_fields['student'].queryset = formset.form.base_fields['student'].queryset.filter(
                student_class=obj.class_marked
            )
        else:
            # If it's a brand new attendance session and no class is selected yet,
            # show an empty queryset so the admin doesn't load thousands of irrelevant students.
            formset.form.base_fields['student'].queryset = formset.form.base_fields['student'].queryset.none()
            
        return formset

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'class_marked', 'marked_by')
    inlines = [AttendanceRecordInline]