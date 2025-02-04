
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from courses.models import Enrollment, Course
from .forms import UserRegisterForm, UserUpdateForm, StatusUpdateForm
from .models import CustomUser

def home(request):
    return render(request, 'home/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('users:login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
    context = {
        'u_form': u_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def update_status(request):
    """
    View to update the single status field on the CustomUser model.
    """
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your status has been updated!')
            return redirect('users:profile')  # or redirect to the user home page if you prefer
    else:
        form = StatusUpdateForm(instance=request.user)
    return render(request, 'users/update_status.html', {'form': form})

@login_required
def user_courses(request):
    if request.user.role == 'Student':
        enrollments = Enrollment.objects.filter(student=request.user)
        courses = [enrollment.course for enrollment in enrollments]
    else:
        courses = Course.objects.filter(teacher=request.user)
    return render(request, 'users/user_courses.html', {'courses': courses})

@require_http_methods(["GET"])
def custom_logout(request):
    logout(request)
    return render(request, 'users/logout.html')

# User home view that shows profile info, courses, and the single status.
@login_required
def user_home(request, username):
    page_user = get_object_or_404(CustomUser, username=username)
    if page_user.role == 'Student':
        enrollments = Enrollment.objects.filter(student=page_user).select_related('course')
        courses = [enrollment.course for enrollment in enrollments]
    else:
        courses = Course.objects.filter(teacher=page_user)

    # For a single status, we simply use the status field from the user model.
    # Optionally, if the logged-in user is viewing their own page, you can let them update it.
    context = {
        'page_user': page_user,
        'courses': courses,
    }
    return render(request, 'users/user_home.html', context)

# DRF ViewSet (if you use it)
from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]