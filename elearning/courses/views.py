from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment, CourseMaterial, CourseFeedback
from .forms import CourseForm, CourseMaterialForm, CourseFeedbackForm
from users.models import CustomUser

@login_required
def course_list(request):
    """
    If teacher, show only their courses;
    if student, show all courses (or all available courses).
    """
    if request.user.is_teacher:
        courses = Course.objects.filter(teacher=request.user)
    else:
        courses = Course.objects.all()  # or filter as needed
    return render(request, 'courses/course_list.html', {'courses': courses})


@login_required
def create_course(request):
    if not request.user.is_teacher:
        messages.error(request, 'Only teachers can create courses.')
        return redirect('courses:course_list')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('courses:course_list')
    else:
        form = CourseForm()

    return render(request, 'courses/create_course.html', {'form': form})


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    materials = course.materials.all()

    # Only teacher for this course can see enrolled students
    enrolled_students = None
    if request.user.is_teacher and course.teacher == request.user:
        enrolled_students = [enr.student for enr in course.enrollments.all()]

    # Handle material upload
    if request.method == 'POST' and 'material_upload' in request.POST:
        if not request.user.is_teacher:
            messages.error(request, 'You do not have permission to upload materials.')
        else:
            mat_form = CourseMaterialForm(request.POST, request.FILES)
            if mat_form.is_valid():
                material = mat_form.save(commit=False)
                material.course = course
                material.save()
                messages.success(request, 'Material uploaded successfully!')
                return redirect('courses:course_detail', pk=pk)
    else:
        mat_form = CourseMaterialForm()

    context = {
        'course': course,
        'materials': materials,
        'mat_form': mat_form,
        'enrolled_students': enrolled_students,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_in_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if not request.user.is_student:
        messages.error(request, 'Teachers cannot enroll in courses.')
        return redirect('courses:course_detail', pk=pk)

    # Check if already enrolled
    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info(request, 'You are already enrolled in this course.')
    else:
        Enrollment.objects.create(student=request.user, course=course)
        messages.success(request, 'You have enrolled in the course.')
    return redirect('courses:course_detail', pk=pk)


@login_required
def leave_feedback(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        form = CourseFeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = request.user
            feedback.save()
            messages.success(request, 'Thank you for your feedback!')
            return redirect('courses:course_detail', pk=pk)
    else:
        form = CourseFeedbackForm()
    return render(request, 'courses/feedback_form.html', {'form': form, 'course': course})


@login_required
def block_student(request, course_id, student_id):
    course = get_object_or_404(Course, id=course_id, teacher=request.user)
    enrollment = get_object_or_404(Enrollment, course=course, student__id=student_id)
    enrollment.delete()  # Or set a flag is_blocked=True
    messages.success(request, 'The student has been blocked/removed from this course.')
    return redirect('courses:course_detail', pk=course_id)