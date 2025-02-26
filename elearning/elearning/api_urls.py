# elearning/api_urls.py
from rest_framework.routers import DefaultRouter
from users.api_views import CustomUserViewSet
from courses.api_views import CourseViewSet, EnrollmentViewSet, FeedbackViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('courses', CourseViewSet, basename='courses')
router.register('enrollments', EnrollmentViewSet, basename='enrollments')
router.register('feedback', FeedbackViewSet, basename='feedback')

urlpatterns = router.urls