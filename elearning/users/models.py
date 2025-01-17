from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Define user roles
    STUDENT = 'Student'
    TEACHER = 'Teacher'
    ROLE_CHOICES = [
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]

    # Add additional fields
    real_name = models.CharField(max_length=150)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='default.jpg')
    role = models.CharField(max_length=7, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username