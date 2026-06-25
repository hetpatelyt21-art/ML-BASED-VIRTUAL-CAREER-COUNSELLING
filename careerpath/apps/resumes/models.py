from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class ResumeAnalysis(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resume_analyses")
    target_role = models.CharField(max_length=140)
    resume_file = models.FileField(upload_to="resume_analyses/")
    original_filename = models.CharField(max_length=255, blank=True)
    extracted_text = models.TextField(blank=True)
    ats_score = models.PositiveIntegerField(default=0)
    keyword_matches = models.JSONField(default=list, blank=True)
    missing_keywords = models.JSONField(default=list, blank=True)
    weak_bullets = models.JSONField(default=list, blank=True)
    formatting_issues = models.JSONField(default=list, blank=True)
    improvement_suggestions = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} resume analysis ({self.ats_score})"

