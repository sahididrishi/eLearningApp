import pytest
from users.serializers import CustomUserSerializer
from users.models import CustomUser

@pytest.mark.django_db
def test_user_serializer_create_positive():
    data = {
        'username': 'serializerUser',
        'role': 'Student',
        'real_name': 'Serializer Test'
    }
    serializer = CustomUserSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    user = serializer.save()
    assert user.username == 'serializerUser'

@pytest.mark.django_db
def test_user_serializer_missing_username_negative():
    data = {'role': 'Student', 'real_name': 'NoUsername'}
    serializer = CustomUserSerializer(data=data)
    assert not serializer.is_valid()
    assert 'username' in serializer.errors