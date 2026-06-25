from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class RoleCommunity(TimeStampedModel):
    name = models.CharField(max_length=140, unique=True)
    target_role = models.CharField(max_length=140)
    description = models.TextField(blank=True)


class ProjectShowcase(TimeStampedModel):
    community = models.ForeignKey(RoleCommunity, on_delete=models.CASCADE, related_name="showcases")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_showcases")
    title = models.CharField(max_length=180)
    project_url = models.URLField(blank=True)
    summary = models.TextField()
