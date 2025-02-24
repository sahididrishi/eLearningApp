
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, CourseMaterial, Notification

@receiver(post_save, sender=Enrollment)
def notify_teacher_on_enrollment(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        teacher = course.teacher
        message = f"{instance.student.username} has enrolled in your course '{course.title}'."
        Notification.objects.create(recipient=teacher, message=message)

@receiver(post_save, sender=CourseMaterial)
def notify_students_on_new_material(sender, instance, created, **kwargs):
    if created:
        course = instance.course
        message = f"New material '{instance.title}' has been added to course '{course.title}'."
        # For each enrollment in the course, notify the student
        for enrollment in course.enrollments.all():
            Notification.objects.create(recipient=enrollment.student, message=message)