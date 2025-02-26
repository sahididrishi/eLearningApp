from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'real_name', 'role', 'status', 'profile_picture']
        # Note: Exclude sensitive fields like password.