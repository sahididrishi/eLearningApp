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

#FeedbackForm
RATING_CHOICES = [
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
]

class FeedbackForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.RadioSelect(),
        label='Rating'
    )

    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        labels = {
            'comment': 'Comment',
        }