from django import forms

from .models import ResumeEducation, ResumeExperience, ResumeProfile


class ResumeProfileForm(forms.ModelForm):
    class Meta:
        model = ResumeProfile
        fields = [
            "headline",
            "summary",
            "location",
            "phone",
            "linkedin_url",
            "github_url",
            "portfolio_url",
        ]


class ResumeEducationForm(forms.ModelForm):
    class Meta:
        model = ResumeEducation
        fields = ["institution", "degree", "start_year", "end_year", "description"]


class ResumeExperienceForm(forms.ModelForm):
    class Meta:
        model = ResumeExperience
        fields = ["title", "organization", "start_date", "end_date", "description"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
