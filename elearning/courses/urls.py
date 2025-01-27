# courses/urls.py
from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path('create/', views.create_course, name='create-course'),
    path('browse/', views.browse_courses, name='browse-courses'),
    path('<int:course_id>/', views.course_detail, name='course-detail'),
    path('<int:course_id>/enroll/', views.enroll_course, name='enroll-course'),
    path('<int:course_id>/update/', views.update_course, name='update-course'),
    path('<int:course_id>/delete/', views.delete_course, name='delete-course'),
    path('<int:course_id>/students/', views.view_enrolled_students, name='view-enrolled-students'),
    path('<int:course_id>/upload-material/', views.upload_material, name='upload-material'),
]