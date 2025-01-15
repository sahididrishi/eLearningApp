from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, StatusUpdateForm
from .models import CustomUser, StatusUpdate


@login_required
def dashboard(request):
    """
    Display a 'dashboard' or 'home' page for the logged-in user.
    Optionally, you can replicate your status updates logic here.
    """
    status_form = StatusUpdateForm(request.POST or None)
    if request.method == 'POST' and status_form.is_valid():
        StatusUpdate.objects.create(
            user=request.user,
            content=status_form.cleaned_data['content']
        )
        return redirect('users:dashboard')

    user_updates = request.user.status_updates.all().order_by('-created_at')
    return render(request, 'users/dashboard.html', {
        'user_updates': user_updates,
        'status_form': status_form,
    })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:dashboard', username=user.username)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


def user_logout(request):
    logout(request)
    return redirect('users:login')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to 'dashboard' WITHOUT passing username
            return redirect('users:dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})

@login_required
def home(request, username):
    """
    A home page for a particular user, showing their status updates, etc.
    """
    profile_user = get_object_or_404(CustomUser, username=username)

    if request.method == 'POST':
        form = StatusUpdateForm(request.POST)
        if form.is_valid():
            StatusUpdate.objects.create(
                user=request.user,
                content=form.cleaned_data['content']
            )
            return redirect('users:dashboard', username=request.user.username)
    else:
        form = StatusUpdateForm()

    status_updates = profile_user.status_updates.all().order_by('-created_at')

    return render(request, 'users/home.html', {
        'profile_user': profile_user,
        'status_updates': status_updates,
        'form': form,
    })