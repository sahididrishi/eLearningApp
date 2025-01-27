# courses/admin.py
from django.contrib import admin
from .models import Course, Enrollment, CourseMaterial

class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'created_at']
    search_fields = ['title', 'description']
    list_filter = ['teacher', 'created_at']

class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at']
    search_fields = ['student__username', 'course__title']
    list_filter = ['enrolled_at']

class CourseMaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'uploaded_at']
    search_fields = ['title', 'course__title']
    list_filter = ['uploaded_at']

admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(CourseMaterial, CourseMaterialAdmin)