
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.decorators import teacher_required, student_required
from .models import Course, Enrollment, CourseMaterial
from .forms import CourseForm, CourseMaterialForm

@login_required
@teacher_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses:course-detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def browse_courses(request):
    courses = Course.objects.all()
    return render(request, 'courses/browse_courses.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    is_enrolled = False
    if request.user.role == 'Student':
        is_enrolled = Enrollment.objects.filter(student=request.user, course=course).exists()

    materials = course.materials.all()
    if request.user.role == 'Student' and not is_enrolled:
        messages.error(request, 'You must enroll in this course to view its materials.')
        return redirect('courses:browse-courses')

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'is_enrolled': is_enrolled,
        'materials': materials
    })

@login_required
@student_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
    if created:
        messages.success(request, f'You have successfully enrolled in {course.title}!')
    else:
        messages.info(request, f'You are already enrolled in {course.title}.')
    return redirect('courses:course-detail', course_id=course.id)

@login_required
@teacher_required
def update_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('courses:course-detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'courses/update_course.html', {'form': form, 'course': course})

@login_required
@teacher_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('courses:browse-courses')
    return render(request, 'courses/delete_course.html', {'course': course})

@login_required
@teacher_required
def view_enrolled_students(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollments = course.enrollments.select_related('student')
    return render(request, 'courses/view_enrolled_students.html', {
        'course': course,
        'enrollments': enrollments
    })

@login_required
@teacher_required
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            messages.success(request, 'Material uploaded successfully!')
            return redirect('courses:course-detail', course_id=course.id)
    else:
        form = CourseMaterialForm()
    return render(request, 'courses/upload_material.html', {'form': form, 'course': course})

# DRF ViewSet
from rest_framework import viewsets, permissions
from .serializers import CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # If teacher is always current user
        serializer.save(teacher=self.request.user)