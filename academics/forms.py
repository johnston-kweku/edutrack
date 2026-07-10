from django import forms
from .models import Class, Subject, ClassSubject, Term, AcademicYear, Assessment, AssessmentRecord


class ClassCreationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            'level', 'stage', 'class_teacher'
        ]


class SubjectCreationForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
            'name'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-50 focus:border-blue-600 focus:bg-white text-gray-900 font-medium transition-all outline-none placeholder-gray-400',
                'placeholder': 'e.g. Mathematics'
            })
        }


class ClassSubjectCreationForm(forms.ModelForm):
    class Meta:
        model = ClassSubject
        fields = [
            'subject', 'subject_class', 'teacher'
        ]
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-50 focus:border-blue-600 focus:bg-white text-gray-900 font-medium appearance-none transition-all outline-none cursor-pointer'
            }),
            'subject_class': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-50 focus:border-blue-600 focus:bg-white text-gray-900 font-medium appearance-none transition-all outline-none cursor-pointer'
            }),
            'teacher': forms.Select(attrs={
                'class': 'block w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-50 focus:border-blue-600 focus:bg-white text-gray-900 font-medium appearance-none transition-all outline-none cursor-pointer'
            })
        }





class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = ['start_year', 'end_year', 'is_current']

    def clean(self):
        cleaned_data = super().clean()
        start_year = cleaned_data.get('start_year')
        end_year = cleaned_data.get('end_year')

        if start_year and end_year and end_year != start_year + 1:
            self.add_error('end_year', 'End year must be exactly one year after the start year.')

        return cleaned_data


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['term', 'academic_year', 'is_current']