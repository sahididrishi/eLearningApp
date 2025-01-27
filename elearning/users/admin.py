# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('real_name', 'profile_picture', 'role')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('real_name', 'profile_picture', 'role')}),
    )
    list_display = ['username', 'email', 'real_name', 'role', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)