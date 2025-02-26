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

# Form to update the single status field
class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['status']
        widgets = {
            'status': forms.Textarea(attrs={'rows': 2, 'placeholder': "What's on your mind?"})
        }


class UserSearchForm(forms.Form):
    query = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by username or real name'
        })
    )
    role = forms.ChoiceField(
        required=False,
        choices=[('', 'Any'), ('Student', 'Student'), ('Teacher', 'Teacher')],
        widget=forms.Select()
    )