import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import CustomUser

@pytest.mark.django_db
def test_teacher_can_list_users_positive():
    teacher = CustomUser.objects.create_user(username='teacher', password='pass', role='Teacher')
    student = CustomUser.objects.create_user(username='stud', password='pass', role='Student')
    client = APIClient()
    client.login(username='teacher', password='pass')

    url = reverse('users-list')  # e.g. /api/users/
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 2  # teacher sees multiple users

@pytest.mark.django_db
def test_student_can_only_see_self_negative():
    teacher = CustomUser.objects.create_user(username='teacher', password='pass', role='Teacher')
    student = CustomUser.objects.create_user(username='stud', password='pass', role='Student')
    client = APIClient()
    client.login(username='stud', password='pass')

    url = reverse('users-list')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1  # only see themselves
    assert response.data[0]['username'] == 'stud'