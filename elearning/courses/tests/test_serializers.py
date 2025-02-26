import pytest
from courses.models import Course, Feedback
from courses.serializers import CourseSerializer, FeedbackSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_course_serializer_positive():
    teacher = User.objects.create_user(username='teach', role='Teacher')
    data = {'title': 'Serialized Course', 'description': 'Desc', 'teacher': teacher.id}
    serializer = CourseSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    course = serializer.save()
    assert course.title == 'Serialized Course'

@pytest.mark.django_db
def test_feedback_serializer_invalid_rating_negative():
    data = {'comment': 'Test', 'rating': 999}
    serializer = FeedbackSerializer(data=data)
    assert not serializer.is_valid()
    assert 'rating' in serializer.errors