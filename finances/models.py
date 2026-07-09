from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ValidationError
from academics.models import Student, Class, Term
User = get_user_model()
# Create your models here.



class Fee(models.Model):
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    student_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f'{self.student_class}– {self.amount}'
    

    class Meta:
        unique_together = ['student_class', 'term']

class FeePayment(models.Model):
    fee = models.ForeignKey(Fee, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    amount_tendered = models.DecimalField(max_digits=6, decimal_places=2)
    paid_at = models.DateTimeField(default=timezone.now)
    received_by = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'role__in': ['ADMIN', 'TEACHING_STAFF']})
    balance = models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    def __str__(self):
        return f'{self.student.student_name} – {self.balance}'

    def save(self, *args, **kwargs):
        previous_payments = FeePayment.objects.filter(
            student=self.student,
            fee=self.fee
        ).exclude(pk=self.pk).aggregate(total=Sum('amount_tendered'))['total'] or 0
        self.balance = self.fee.amount - previous_payments - self.amount_tendered
        

        if previous_payments + self.amount_tendered > self.fee.amount:
            raise ValidationError(f'Cannot pay more than fee amount – {self.fee.amount}')

        super().save(*args, **kwargs)

