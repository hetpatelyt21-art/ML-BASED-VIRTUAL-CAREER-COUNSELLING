from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class MentorConversation(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mentor_conversations")
    title = models.CharField(max_length=160, default="Career mentor session")
    target_role = models.CharField(max_length=140, blank=True)

    class Meta:
        ordering = ["-updated_at"]


class MentorMessage(TimeStampedModel):
    ROLE_CHOICES = [("user", "User"), ("assistant", "Assistant"), ("system", "System")]

    conversation = models.ForeignKey(MentorConversation, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)
    content = models.TextField()
    provider = models.CharField(max_length=40, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["created_at"]

