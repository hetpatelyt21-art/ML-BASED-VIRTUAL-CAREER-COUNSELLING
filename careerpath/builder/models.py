from django.contrib.auth.models import User
from django.db import models


class ResumeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="resume_profile")
    headline = models.CharField(max_length=160, blank=True)
    summary = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    linkedin_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)


class ResumeEducation(models.Model):
    resume_profile = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE, related_name="education_items"
    )
    institution = models.CharField(max_length=160)
    degree = models.CharField(max_length=160)
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_year", "-id"]


class ResumeExperience(models.Model):
    resume_profile = models.ForeignKey(
        ResumeProfile, on_delete=models.CASCADE, related_name="experience_items"
    )
    title = models.CharField(max_length=160)
    organization = models.CharField(max_length=160)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-start_date", "-id"]

