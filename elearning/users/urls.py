from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "users"

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),

    # Use your custom login or django's auth_views
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),

    path('profile/', views.profile, name='profile'),
    path('update-status/', views.update_status, name='update-status'),
    path('courses/', views.user_courses, name='user_courses'),
    path('logout/', views.custom_logout, name='logout'),

    # NEW route for the user's public home page

    path('search/', views.search_users, name='search-users'),
    path('<str:username>/', views.user_home, name='user-home'),
]