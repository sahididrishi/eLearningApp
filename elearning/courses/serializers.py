
from rest_framework import serializers
from .models import Course

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.ReadOnlyField(source='teacher.real_name')

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher_name', 'created_at']