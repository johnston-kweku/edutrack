# academics/migrations/00XX_set_next_class_chain.py
from django.db import migrations

CHAIN = [
    ('KINDERGARTEN', '1'), ('KINDERGARTEN', '2'),
    ('LOWER_PRIMARY', '1'), ('LOWER_PRIMARY', '2'), ('LOWER_PRIMARY', '3'),
    ('UPPER_PRIMARY', '4'), ('UPPER_PRIMARY', '5'), ('UPPER_PRIMARY', '6'),
    ('JHS', '1'), ('JHS', '2'), ('JHS', '3'),
]

def set_chain(apps, schema_editor):
    Class = apps.get_model('academics', 'Class')
    for i in range(len(CHAIN) - 1):
        level, stage = CHAIN[i]
        next_level, next_stage = CHAIN[i + 1]
        try:
            current = Class.objects.get(level=level, stage=stage)
            nxt = Class.objects.get(level=next_level, stage=next_stage)
            current.next_class = nxt
            current.save()
        except Class.DoesNotExist:
            pass  # class not created yet, skip

def reverse_chain(apps, schema_editor):
    Class = apps.get_model('academics', 'Class')
    Class.objects.update(next_class=None)

class Migration(migrations.Migration):
    dependencies = [
        ('academics', '0031_class_next_class'),  # replace with your actual prior migration name
    ]
    operations = [
        migrations.RunPython(set_chain, reverse_chain),
    ]