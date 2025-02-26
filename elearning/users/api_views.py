from rest_framework import viewsets, permissions
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for CustomUser.
    Teachers can view all users; students can view only themselves.
    POST is allowed if you want to enable user creation via API.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Teacher':
            return CustomUser.objects.all()
        else:
            return CustomUser.objects.filter(pk=user.pk)