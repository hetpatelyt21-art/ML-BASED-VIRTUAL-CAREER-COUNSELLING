from django import forms
from core.ml.basic_test_questions import basic_test_questions
from .models import UserProfile

LIKERT_CHOICES = [(i, str(i)) for i in range(1, 6)]

class BasicTestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for q_num, question in basic_test_questions.items():
            self.fields[f"Q{q_num}"] = forms.ChoiceField(
                label=question,
                choices=LIKERT_CHOICES,
                widget=forms.HiddenInput
            )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_photo', 'age', 'education_level', 'preferred_field']
        widgets = {
            'profile_photo': forms.FileInput(attrs={
                'class': 'form-control-file custom-file-input'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your age'
            }),
            'education_level': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Graduate'
            }),
            'preferred_field': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Law, Medicine'
            }),
        }
