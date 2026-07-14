from django.contrib import admin
from .models import Fee, FeePayment

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ['student_class', 'term', 'amount', 'description']
    list_filter = ['term', 'student_class']

@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ['student', 'fee', 'amount_tendered', 'balance', 'paid_at', 'received_by']
    list_filter = ['paid_at']
    search_fields = ['student__student_name']