# elearning_project/api_urls.py
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet
from courses.views import CourseViewSet

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='user')
router.register('courses', CourseViewSet, basename='course')

urlpatterns = router.urls