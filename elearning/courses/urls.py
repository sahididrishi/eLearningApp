from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.course_list, name='course_list'),           # /courses/
    path('create/', views.create_course, name='create_course'),# /courses/create/
    path('<int:pk>/', views.course_detail, name='course_detail'),    # /courses/1/
    path('<int:pk>/enroll/', views.enroll_in_course, name='enroll'), # /courses/1/enroll/
    path('<int:pk>/feedback/', views.leave_feedback, name='leave_feedback'), # /courses/1/feedback/
    path('<int:course_id>/block/<int:student_id>/', views.block_student, name='block_student'),
]