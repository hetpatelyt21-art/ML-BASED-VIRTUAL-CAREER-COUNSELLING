from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class MockInterview(TimeStampedModel):
    ROLE_CHOICES = [
        ("Software Engineer", "Software Engineer"),
        ("Data Scientist", "Data Scientist"),
        ("UI/UX Designer", "UI/UX Designer"),
        ("Business Analyst", "Business Analyst"),
        ("Product Manager", "Product Manager"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mock_interviews")
    target_role = models.CharField(max_length=80, choices=ROLE_CHOICES)
    overall_score = models.PositiveIntegerField(default=0)
    confidence_score = models.PositiveIntegerField(default=0)
    weak_topics = models.JSONField(default=list, blank=True)
    feedback = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]


class InterviewQuestion(TimeStampedModel):
    interview = models.ForeignKey(MockInterview, on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    answer = models.TextField(blank=True)
    score = models.PositiveIntegerField(default=0)
    feedback = models.TextField(blank=True)
    topic = models.CharField(max_length=120, blank=True)

