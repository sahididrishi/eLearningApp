from django.test import TestCase
from django.urls import reverse
from courses.models import Course
from users.models import CustomUser

class CourseViewsTest(TestCase):
    def setUp(self):
        self.teacher = CustomUser.objects.create_user(username='teacher', password='pass', role='Teacher')
        self.student = CustomUser.objects.create_user(username='student', password='pass', role='Student')
        self.create_url = reverse('courses:create-course')

    def test_teacher_create_course_positive(self):
        self.client.login(username='teacher', password='pass')
        data = {'title': 'View Course', 'description': 'Desc'}
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(title='View Course').exists())

    def test_student_create_course_negative(self):
        self.client.login(username='student', password='pass')
        data = {'title': 'Nope', 'description': 'Denied'}
        response = self.client.post(self.create_url, data)
        self.assertNotEqual(response.status_code, 200)  # Possibly 403 or redirect

    def test_student_cannot_upload_material_negative(self):
        self.client.login(username='student', password='pass')
        course = Course.objects.create(title='Test Course', description='Desc', teacher=self.teacher)
        url = reverse('courses:upload-material', args=[course.id])
        data = {'title': 'Material', 'file': ''}  # or an invalid file
        response = self.client.post(url, data)
        self.assertNotEqual(response.status_code, 200)  # 403 or redirect