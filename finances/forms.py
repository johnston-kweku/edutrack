from django import forms
from django.forms import DateTimeInput
from django.db.models import Sum
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
        fields = ['fee', 'student', 'amount_tendered', 'paid_at']
        widgets = {
            'paid_at': DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }


    def clean(self):
        cleaned_data = super().clean()
        fee = cleaned_data.get('fee')
        student = cleaned_data.get('student')
        amount_tendered = cleaned_data.get('amount_tendered')

        # If any required field is missing/invalid already, skip this check —
        # individual field errors will already be shown, no need to pile on
        if fee is None or student is None or amount_tendered is None:
            return cleaned_data

        previous_payments = FeePayment.objects.filter(
            student=student,
            fee=fee
        ).exclude(pk=self.instance.pk).aggregate(
            total=Sum('amount_tendered')
        )['total'] or 0

        if previous_payments + amount_tendered > fee.amount:
            remaining = fee.amount - previous_payments
            self.add_error(
                'amount_tendered',
                f'This payment exceeds what is owed. Remaining balance: {remaining}'
            )

        return cleaned_data