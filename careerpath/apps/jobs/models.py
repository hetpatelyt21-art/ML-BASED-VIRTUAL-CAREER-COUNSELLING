from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Opportunity(TimeStampedModel):
    TYPE_CHOICES = [("internship", "Internship"), ("job", "Fresher Job"), ("remote", "Remote Job")]

    title = models.CharField(max_length=180)
    company = models.CharField(max_length=160)
    opportunity_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    location = models.CharField(max_length=120, blank=True)
    remote = models.BooleanField(default=False)
    source_url = models.URLField(blank=True)
    required_skills = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]


class MatchScore(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_matches")
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name="matches")
    skill_match_percentage = models.PositiveIntegerField(default=0)
    resume_match_percentage = models.PositiveIntegerField(default=0)
    overall_match_percentage = models.PositiveIntegerField(default=0)
    missing_skills = models.JSONField(default=list, blank=True)

    class Meta:
        unique_together = ("user", "opportunity")
        ordering = ["-overall_match_percentage"]

