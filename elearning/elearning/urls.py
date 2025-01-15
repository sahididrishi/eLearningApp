from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from rest_framework import routers
from users.api import CustomUserViewSet

router = routers.DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users_api')

def home_redirect(request):
    """
    If someone hits the root URL `/`, just redirect them
    to the login page or any other page you prefer.
    """
    return redirect('users:login')

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users app
    path('accounts/', include('users.urls', namespace='users')),

    # Courses app
    path('courses/', include('courses.urls', namespace='courses')),

    # Chat app
    path('chat/', include('chat.urls', namespace='chat')),

    path('api/', include(router.urls)),  # DRF routes

    path('', home_redirect, name='root_redirect'),

]