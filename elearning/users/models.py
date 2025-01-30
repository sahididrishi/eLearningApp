
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    STUDENT = 'Student'
    TEACHER = 'Teacher'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]

    real_name = models.CharField(max_length=150, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default=STUDENT)

    def __str__(self):
        return self.username