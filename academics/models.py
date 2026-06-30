from django.db import models, transaction
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os
User = get_user_model()

# Create your models here.
class Class(models.Model):
    class Stage(models.TextChoices):
        ONE = '1', '1'
        TWO = '2', '2'
        THREE = '3', '3'
        FOUR = '4', '4'
        FIVE = '5', '5'
        SIX = '6', '6'

    class Level(models.TextChoices):
        JHS = 'JHS'
        KINDERGARTEN = 'KINDERGARTEN', 'KG'
        LOWER_PRIMARY = 'LOWER_PRIMARY', 'Lower Primary'
        UPPER_PRIMARY = 'UPPER_PRIMARY', 'Upper Primary'
        
    stage = models.CharField(max_length=20, choices=Stage.choices)
    level = models.CharField(max_length=20, choices=Level.choices)
    class_teacher = models.OneToOneField(User, on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'role__in': ['TEACHING_STAFF', 'ADMIN']}, related_name='class_assigned')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.level} {self.stage}'
    
    class Meta:
        verbose_name_plural = 'Classes'
        unique_together = ['level', 'stage']
        ordering = ['stage']

    def clean(self):
        valid_stages = {
            'KINDERGARTEN': ['1', '2'],
            'LOWER_PRIMARY': ['1', '2', '3'],
            'UPPER_PRIMARY': ['4', '5', '6'],
            'JHS': ['1', '2', '3']
        }        

        allowed = valid_stages.get(self.level, [])
        if self.stage not in allowed:
            raise ValidationError(f'{self.get_level_display()} {self.stage} is not a valid class')
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)



class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)


    def __str__(self):
        return f'{self.name}'
    

class ClassSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    subject_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    teacher = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, limit_choices_to={'role__in': ['TEACHING_STAFF', 'ADMIN']})
    

    class Meta:
        unique_together = [ 'subject', 'subject_class' ]

    def __str__(self):
        return f'{self.subject} – {self.subject_class}'
    

class AcademicYear(models.Model):
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.start_year}/{self.end_year}'
    
    def save(self, *args, **kwargs):
        if self.is_current:
            with transaction.atomic():
                AcademicYear.objects.select_for_update().filter(is_current=True).exclude(pk=self.pk).update(is_current=False)

        super().save(*args, **kwargs)


class Term(models.Model):
    class Terms(models.TextChoices):
        ONE = '1', '1'
        TWO = '2', '2'
        THREE = '3', '3'

    term = models.CharField(max_length=20, choices=Terms.choices)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    is_current = models.BooleanField(default=False)

    class Meta:
        unique_together = ['term', 'academic_year']

    def __str__(self):
        return f'TERM: {self.term}'
    

    def save(self, *args, **kwargs):
        if self.is_current:
            with transaction.atomic():
                Term.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        
        super().save(*args, **kwargs)



class Student(models.Model):
    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    student_id = models.CharField(max_length=50, unique=True, blank=True)
    student_name = models.CharField(max_length=500)
    student_class = models.ForeignKey(Class, on_delete=models.PROTECT, related_name='student')
    date_of_birth = models.DateField()
    enrollment_date = models.DateField(auto_now_add=True)
    gender = models.CharField(max_length=20, choices=Gender.choices)
    parent = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'role': 'PARENT'}, blank=True, null=True, related_name='student')
    image = models.ImageField(upload_to='student_images/', blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg'])])


    def __str__(self):
        return self.student_name
    
    def save(self, *args, **kwargs):

        is_new = self.pk is None
        if is_new:
            # Save initially to populate self.pk
            super().save(*args, **kwargs)
            

            self.student_id = f'STU-{str(self.pk).zfill(5)}'
            # Save the student_id back to the instance
            super().save(update_fields=['student_id'])

        # Track if a new image was actually uploaded to avoid re-compressing
        if self.image:
            if not is_new:
                # Grab the original image from the database to compare
                orig = Student.objects.get(pk=self.pk)
                image_changed = orig.image != self.image
            else:
                image_changed = True

            if image_changed:
                

                img = Image.open(self.image)
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                max_size = (600, 600)
                img.thumbnail(max_size)

                buffer = BytesIO()
                img.save(buffer, format='JPEG', quality=70, optimize=True)
                buffer.seek(0)

                name = os.path.splitext(os.path.basename(self.image.name))[0] + '.jpg'
                self.image = ContentFile(buffer.read(), name=name)
                
                # If it's not a new instance, we need to make sure this gets saved
                if not is_new:
                    super().save(*args, **kwargs)

        # Fallback save for standard updates (if not already handled)
        if not is_new and not 'image_changed' in locals():
            super().save(*args, **kwargs)




class Assessment(models.Model):
    class AssessmentType(models.TextChoices):
        QUIZ = 'QUIZ', 'Quiz'
        CLASS_TEST = 'CLASS TEST', 'Class Test'
        EXAM = 'EXAM', 'Exam'
        EXERCISE = 'EXERCISE', 'Exercise'
    date = models.DateTimeField(default=timezone.now)
    assessment_type = models.CharField(max_length=30, choices=AssessmentType.choices)
    recorded_by = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'role__in': ['TEACHING_STAFF', 'ADMIN']})
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    term = models.ForeignKey(Term, on_delete=models.PROTECT)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT)
    student_class = models.ForeignKey(Class, on_delete=models.PROTECT)
    max_score = models.DecimalField(max_digits=5, decimal_places=2) 

    def __str__(self):
        return f'{self.assessment_type} – {self.term} – {self.academic_year}'


class AssessmentRecord(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    score = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.student} – {self.score}'
    
    class Meta:
        unique_together = ['student', 'assessment']

    def save(self, *args, **kwargs):

        if self.score < 0 or self.score > self.assessment.max_score:
            raise ValidationError(f'Score must be between 0 and {self.assessment.max_score} for {self.assessment.assessment_type}')
        super().save(*args, **kwargs)
        



class Attendance(models.Model):
    date = models.DateField(default=timezone.now, editable=False)
    class_marked = models.ForeignKey(Class, on_delete=models.PROTECT, null=True)
    marked_by = models.ForeignKey(User, on_delete=models.PROTECT, limit_choices_to={'role__in': ['TEACHING_STAFF', 'ADMIN']})

    def __str__(self):
        return f'Attendance on {self.date} for {self.class_marked} by {self.marked_by}'
    

    class Meta:
        verbose_name_plural = 'Attendance'
        unique_together = ['class_marked', 'date']



class AttendanceRecord(models.Model):
    attendance = models.ForeignKey(Attendance, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    is_present = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        student_name = self.student.name.split(' ')[0]
        status = 'Present' if self.is_present else 'Absent'
        return f'{student_name} – {status}'
    

    class Meta:
        unique_together = ['student', 'attendance'] 

