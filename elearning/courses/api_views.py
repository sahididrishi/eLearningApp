from rest_framework import viewsets, permissions
from .models import Course, Enrollment, Feedback
from .serializers import CourseSerializer, EnrollmentSerializer, FeedbackSerializer

from users.permissions import IsTeacher

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for courses.
    Teachers can create/update/delete courses; students can view courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsTeacher]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        # Automatically set the current user as teacher when creating a course.
        serializer.save(teacher=self.request.user)

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for enrollments.
    Students can enroll in courses via POST, and view their enrollments.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Teachers can view all enrollments; students only their own.
        if user.role == 'Teacher':
            return Enrollment.objects.all()
        else:
            return Enrollment.objects.filter(student=user)

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for feedback.
    Students can submit feedback via POST; teachers can view feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # Optionally: teachers see feedback for their courses; students see only their own feedback.
        if user.role == 'Teacher':
            return Feedback.objects.filter(course__teacher=user)
        else:
            return Feedback.objects.filter(student=user)

    def perform_create(self, serializer):
        # Automatically associate the feedback with the current user.
        serializer.save(student=self.request.user)