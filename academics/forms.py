from django import forms
from .models import Class


class ClassCreationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            'level', 'stage', 'class_teacher'
        ]