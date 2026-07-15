from django.db import migrations

def backfill_receipt_numbers(apps, schema_editor):
    FeePayment = apps.get_model('finances', 'FeePayment')
    for payment in FeePayment.objects.filter(receipt_number=''):
        payment.receipt_number = f'RCT-{str(payment.pk).zfill(5)}'
        payment.save(update_fields=['receipt_number'])

class Migration(migrations.Migration):
    dependencies = [
        ('finances', '0003_feepayment_receipt_number_and_more'),
    ]
    operations = [
        migrations.RunPython(backfill_receipt_numbers, migrations.RunPython.noop),
    ]