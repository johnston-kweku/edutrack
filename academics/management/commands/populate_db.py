import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academics.models import Class, Student, AcademicYear, Term, Subject
from django.db import transaction

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with realistic Ghanaian sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')
        
        first_names = [
            'Kofi', 'Ama', 'Kwame', 'Akosua', 'Kwesi', 'Abena', 'Kwaku', 'Akua', 
            'Yaw', 'Yaa', 'Ekow', 'Araba', 'Efua', 'Kojo', 'Adjoa', 'Panyin', 'Kakra'
        ]
        last_names = [
            'Mensah', 'Annan', 'Owusu', 'Adu', 'Appiah', 'Boateng', 'Osei', 'Gyamfi', 
            'Tetteh', 'Quansah', 'Addo', 'Darko', 'Kyei', 'Asante', 'Baah', 'Agyemang'
        ]

        try:
            with transaction.atomic():
                # 1. Create Academic Structure
                year, _ = AcademicYear.objects.get_or_create(start_year=2026, end_year=2027, is_current=True)
                term, _ = Term.objects.get_or_create(term='1', academic_year=year, is_current=True)
                
                subjects = ['Mathematics', 'English Language', 'Science', 'Social Studies', 'ICT', 'RME', 'Creative Arts']
                for name in subjects:
                    Subject.objects.get_or_create(name=name)

                # 2. Create Teachers
                teachers = []
                for i in range(1, 11):
                    username = f'teacher_{i}'
                    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(
                            username=username,
                            email=f'{username}@edutrack.edu',
                            password='password123',
                            full_name=full_name,
                            role='TEACHING_STAFF'
                        )
                        teachers.append(user)
                    else:
                        teachers.append(User.objects.get(username=username))

                # 3. Create Parents
                parents = []
                for i in range(1, 21):
                    username = f'parent_{i}'
                    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
                    contact = f"054{random.randint(1000000, 9999999)}"
                    if not User.objects.filter(username=username).exists():
                        user = User.objects.create_user(
                            username=username,
                            email=f'{username}@mail.com',
                            password='password123',
                            full_name=full_name,
                            role='PARENT',
                            contact=contact
                        )
                        parents.append(user)
                    else:
                        parents.append(User.objects.get(username=username))

                # 4. Create Classes
                class_objs = []
                levels = [
                    (Class.Level.KINDERGARTEN, ['1', '2']),
                    (Class.Level.LOWER_PRIMARY, ['1', '2', '3']),
                    (Class.Level.UPPER_PRIMARY, ['4', '5', '6']),
                    (Class.Level.JHS, ['1', '2', '3'])
                ]
                
                for level, stages in levels:
                    for stage in stages:
                        teacher = random.choice(teachers)
                        # We use filter().first() or get_or_create to handle unique constraints
                        obj, created = Class.objects.get_or_create(
                            level=level, 
                            stage=stage,
                            defaults={'class_teacher': teacher, 'is_active': True}
                        )
                        class_objs.append(obj)

                # 5. Create Students
                for cls in class_objs:
                    # Clear existing students to avoid bloating if re-run, or just add new ones
                    # cls.student_set.all().delete() # Optional: uncomment if you want a fresh start
                    
                    for _ in range(random.randint(8, 15)):
                        name = f"{random.choice(first_names)} {random.choice(last_names)}"
                        parent = random.choice(parents)
                        
                        # Generate a random DOB between 5 and 15 years ago
                        days_ago = random.randint(365*5, 365*15)
                        dob = date.today() - timedelta(days=days_ago)
                        
                        Student.objects.create(
                            name=name,
                            student_class=cls,
                            date_of_birth=dob,
                            gender=random.choice(['MALE', 'FEMALE']),
                            parent=parent
                        )

            self.stdout.write(self.style.SUCCESS('Successfully populated database with realistic data!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error populating database: {str(e)}'))
