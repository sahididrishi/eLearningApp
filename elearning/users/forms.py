# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    real_name = forms.CharField(max_length=150, required=True)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'real_name', 'role', 'profile_picture', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    real_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'real_name', 'profile_picture']