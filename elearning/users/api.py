# users/api.py
from rest_framework import viewsets
from .models import CustomUser
from .serializers import CustomUserSerializer  # you'd need a serializers.py too

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer