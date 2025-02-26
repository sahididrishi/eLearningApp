
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Teacher':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return _wrapped_view

def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'Student':
            return view_func(request, *args, **kwargs)
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return _wrapped_view