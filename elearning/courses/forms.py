from django import forms
from .models import Course, CourseMaterial, Feedback

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description']

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['title', 'file']

# NEW: FeedbackForm
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']  # Adjust as desired (e.g., just 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your feedback...'}),
        }