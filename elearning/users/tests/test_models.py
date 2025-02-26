import pytest
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_user_creation_positive():
    """Positive: create a user with valid data."""
    user = User.objects.create_user(
        username='testuser',
        password='testpass',
        role='Student',
        real_name='Test User'
    )
    assert user.username == 'testuser'
    assert user.role == 'Student'

@pytest.mark.django_db
def test_user_creation_invalid_role_negative():
    """Negative: create a user with an invalid role."""
    user = User(username='invalidRoleUser', role='Alien')  # Suppose only Student or Teacher are valid
    with pytest.raises(ValidationError):
        user.full_clean()

@pytest.mark.django_db
def test_user_str():
    user = User(username='struser')
    assert str(user) == 'struser'