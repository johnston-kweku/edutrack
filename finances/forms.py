from django import forms
from .models import Fee, FeePayment



class FeeCreationForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = [
            'term', 'amount', 'student_class', 'description'
        ]


class FeeRecordForm(forms.ModelForm):
    class Meta:
        model = FeePayment
        fields = [
            'fee', 'student', 'amount_tendered', 'paid_at', 'received_by'
        ]
