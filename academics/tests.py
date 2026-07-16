from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Class, ClassSubject, Student, Subject


class ResultsAndEditViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='adminuser',
            password='secret123',
            full_name='Admin User',
            role='ADMIN'
        )
        self.subject = Subject.objects.create(name='English')
        self.student_class = Class.objects.create(level='JHS', stage='1')
        self.class_subject = ClassSubject.objects.create(
            subject=self.subject,
            subject_class=self.student_class,
            teacher=self.user,
        )

    def test_results_page_lists_subjects_and_class_subjects_with_edit_links(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('academics:academics_hub'))

        self.assertContains(response, self.subject.name)
        self.assertContains(response, str(self.student_class))
        self.assertContains(response, reverse('academics:edit_subject', args=[self.subject.pk]))
        self.assertContains(response, reverse('academics:edit_class_subject', args=[self.class_subject.pk]))

    def test_edit_subject_updates_subject(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('academics:edit_subject', args=[self.subject.pk]),
            {'name': 'Mathematics'}
        )

        self.assertRedirects(response, reverse('academics:academics_hub'))
        self.subject.refresh_from_db()
        self.assertEqual(self.subject.name, 'Mathematics')

    def test_edit_class_subject_updates_class_subject(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse('academics:edit_class_subject', args=[self.class_subject.pk]),
            {
                'subject': self.subject.pk,
                'subject_class': self.student_class.pk,
                'teacher': self.user.pk,
            }
        )

        self.assertRedirects(response, reverse('academics:academics_hub'))
        self.class_subject.refresh_from_db()
        self.assertEqual(self.class_subject.teacher, self.user)

    def test_edit_student_updates_status_when_existing_image_is_present(self):
        self.client.force_login(self.user)
        parent = get_user_model().objects.create_user(
            username='parentuser',
            password='secret123',
            full_name='Parent User',
            role='PARENT'
        )

        image = Image.new('RGB', (1, 1), color='red')
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        student = Student.objects.create(
            student_name='Jane Doe',
            student_class=self.student_class,
            date_of_birth='2008-01-01',
            gender=Student.Gender.FEMALE,
            parent=parent,
            image=SimpleUploadedFile('student.png', buffer.read(), content_type='image/png'),
            status=Student.Status.ENROLLED,
        )

        response = self.client.post(
            reverse('students:edit_student', args=[student.pk]),
            {
                'student_name': student.student_name,
                'student_class': self.student_class.pk,
                'date_of_birth': student.date_of_birth,
                'gender': student.gender,
                'parent': parent.pk,
                'status': Student.Status.DISMISSED,
            }
        )

        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertEqual(student.status, Student.Status.DISMISSED)
