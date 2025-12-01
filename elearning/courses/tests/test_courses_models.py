import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from courses.models import Course, Feedback

User = get_user_model()

@pytest.mark.django_db
def test_course_str_positive():
    teacher = User.objects.create_user(username='teach', password='pass', role='Teacher')
    course = Course.objects.create(title='Django 101', description='Basics', teacher=teacher)
    assert str(course) == 'Django 101'

@pytest.mark.django_db
def test_feedback_rating_negative():
    student = User.objects.create_user(username='stud', password='pass', role='Student')
    teacher = User.objects.create_user(username='teach2', password='pass', role='Teacher')
    course = Course.objects.create(title='Course Title', teacher=teacher)
    fb = Feedback(course=course, student=student, comment='Nice', rating=999)
    with pytest.raises(ValidationError):
        fb.full_clean()  # rating=999 invalid if max=5