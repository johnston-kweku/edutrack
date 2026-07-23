from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.files.base import ContentFile
from django.urls import reverse
import os
from PIL import Image
from io import BytesIO
import uuid
from datetime import timedelta, time


# Create your models here.
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        TEACHING_STAFF = 'TEACHING_STAFF', 'Teaching Staff'
        PARENT = 'PARENT', 'Parent'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        ON_LEAVE = 'ON LEAVE', 'On Leave'

    class Gender(models.TextChoices):
        MALE = 'MALE', 'Male'
        FEMALE = 'FEMALE', 'Female'

    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=50, choices=Roles.choices)
    contact = models.CharField(max_length=15, blank=True)
    picture = models.ImageField(upload_to='user_pictures/', null=True, blank=True) 
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)


    def __str__(self):
        return f"{self.full_name} – {self.role}" 
    
    def is_admin(self):
        return self.role == self.Roles.ADMIN
    
    def is_teaching_staff(self):
        return self.role == self.Roles.TEACHING_STAFF
    
    def is_parent(self):
        return self.role == self.Roles.PARENT


def default_expiry():
        return timezone.now() + timedelta(hours=48)

class Invitation(models.Model):
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    role = models.CharField(max_length=50, choices=User.Roles.choices)
    expires_at = models.DateTimeField(default=default_expiry)

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()