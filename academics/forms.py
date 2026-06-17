from django import forms
from .models import Student, Class

class StudentCreationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name', 'date_of_birth', 'gender', 'parent', 'student_class'
        ]



class ClassCreationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            'level', 'stage', 'class_teacher'
        ]