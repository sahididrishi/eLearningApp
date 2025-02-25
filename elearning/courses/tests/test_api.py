import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import CustomUser
from courses.models import Course


@pytest.mark.django_db
def test_teacher_can_create_course_api_positive():
    teacher = CustomUser.objects.create_user(username='teach', password='pass', role='Teacher')
    client = APIClient()
    client.login(username='teach', password='pass')

    url = reverse('courses-list')  # e.g., /api/courses/
    data = {'title': 'API Course', 'description': 'API Desc'}
    response = client.post(url, data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_student_cannot_create_course_api_negative():
    student = CustomUser.objects.create_user(username='stud', password='pass', role='Student')
    client = APIClient()
    client.login(username='stud', password='pass')

    url = reverse('courses-list')
    data = {'title': 'Unauthorized', 'description': 'Fail'}
    response = client.post(url, data, format='json')
    assert response.status_code in [403, 401]