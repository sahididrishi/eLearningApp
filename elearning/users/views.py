from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from courses.models import Enrollment, Course

from courses.models import Enrollment
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
    if request.method == 'POST':
        form = StatusUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
    else:
        form = StatusUpdateForm(instance=request.user)

    return render(request, 'users/update_status.html',{'form': form})
@login_required
def user_courses(request):
    if request.user.role =='Student':
        enrollments = Enrollment.objects.filter(student=request.user)
        courses = [enrollments.course for enrollment in enrollments]
    else:
        courses = Course.objects.filter(teacher=request.user)
    return render(request,'users/user_courses.html',{'courses':courses})

@require_http_methods(["GET"])  # Accept only GET; no 405 errors if we want a link-based logout
def custom_logout(request):
    """
    Logs out the user and renders the logout.html confirmation page via a GET request.
    """
    logout(request)
    return render(request, 'users/logout.html')

# DRF ViewSet
from rest_framework import viewsets, permissions
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]