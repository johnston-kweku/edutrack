from django import forms
from .models import Class, Subject, ClassSubject, Term, AcademicYear, Assessment, AssessmentRecord
from django.contrib.auth import get_user_model

User = get_user_model()


class ClassCreationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = [
            'level', 'stage', 'class_teacher'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_teacher'].queryset = User.objects.filter(
            role__in=['TEACHING_STAFF', 'ADMIN'],
            is_active=True
        )


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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(
            role__in=['TEACHING_STAFF', 'ADMIN'],
            is_active=True
        )





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




class AssessmentForm(forms.ModelForm):
    class_subject = forms.ModelChoiceField(
        queryset=ClassSubject.objects.none(), label='Class & Subject'
    )
    class Meta:
        model = Assessment
        fields = ['assessment_type', 'date', 'max_score', 'term', 'academic_year']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is None:
            raise ValueError('AssessmentForm requires a user to determine which ClassSubjects are available.')
        self.fields['class_subject'].queryset = ClassSubject.objects.filter(teacher=user).select_related('teacher' ,'subject_class')

    def save(self, commit=True):
        class_subject = self.cleaned_data['class_subject']
        assessment = super().save(commit=False)
        assessment.subject = class_subject.subject
        assessment.student_class = class_subject.subject_class
        if commit:
            assessment.save()
        return assessment