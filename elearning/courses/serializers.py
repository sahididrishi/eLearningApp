# courses/serializers.py
from rest_framework import serializers
from .models import Course, Enrollment, Feedback


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.ReadOnlyField(source='teacher.real_name')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'teacher_name', 'created_at']


class EnrollmentSerializer(serializers.ModelSerializer):
    student_username = serializers.ReadOnlyField(source='student.username')
    course_title = serializers.ReadOnlyField(source='course.title')

    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'student_username', 'course', 'course_title', 'enrolled_at']


class FeedbackSerializer(serializers.ModelSerializer):
    student_username = serializers.ReadOnlyField(source='student.username')
    rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Feedback
        fields = ['id', 'course', 'student', 'student_username', 'comment', 'rating', 'created_at']