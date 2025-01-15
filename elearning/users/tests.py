from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class UserTests(TestCase):
    def test_create_student(self):
        student = CustomUser.objects.create_user(
            username='test_student',
            password='testpass123',
            is_student=True
        )
        self.assertEqual(student.is_student, True)
        self.assertEqual(student.is_teacher, False)

    def test_user_registration_view(self):
        response = self.client.post(reverse('users:register'), {
            'username': 'newuser',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'is_student': True
        })
        self.assertEqual(response.status_code, 302)  # redirect after registration