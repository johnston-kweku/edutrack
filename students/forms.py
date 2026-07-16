from django import forms
from academics.models import Student

class StudentCreationForm(forms.ModelForm):
    class Meta: 
        model = Student
        fields = [
            'student_name', 'student_class', 'date_of_birth', 'gender', 'parent', 'image', 'status'
        ]

