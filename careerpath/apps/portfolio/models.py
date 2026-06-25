from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class PortfolioProject(TimeStampedModel):
    STATUS_CHOICES = [("idea", "Idea"), ("building", "Building"), ("completed", "Completed")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolio_projects")
    target_role = models.CharField(max_length=140)
    title = models.CharField(max_length=180)
    brief = models.TextField()
    readme_markdown = models.TextField(blank=True)
    skills = models.JSONField(default=list, blank=True)
    github_url = models.URLField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="idea")

    class Meta:
        ordering = ["-updated_at"]

