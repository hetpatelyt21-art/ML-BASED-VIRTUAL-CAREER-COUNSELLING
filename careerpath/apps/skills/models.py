from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Skill(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    category = models.CharField(max_length=80, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class CareerSkillRequirement(TimeStampedModel):
    PRIORITIES = [("high", "High"), ("medium", "Medium"), ("low", "Low")]

    target_role = models.CharField(max_length=140)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="career_requirements")
    required_level = models.PositiveSmallIntegerField(default=3)
    priority = models.CharField(max_length=12, choices=PRIORITIES, default="medium")

    class Meta:
        unique_together = ("target_role", "skill")
        ordering = ["target_role", "-required_level", "skill__name"]

    def __str__(self):
        return f"{self.target_role}: {self.skill}"


class UserSkill(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="skills")
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="user_levels")
    level = models.PositiveSmallIntegerField(default=1)
    evidence = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "skill")
        ordering = ["skill__name"]

    def __str__(self):
        return f"{self.user}: {self.skill} ({self.level})"


class SkillGapReport(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="skill_gap_reports")
    assessment_result = models.OneToOneField(
        "website.AssessmentResult",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="skill_gap_report",
    )
    target_role = models.CharField(max_length=140)
    readiness_percentage = models.PositiveIntegerField(default=0)
    missing_skills = models.JSONField(default=list, blank=True)
    priority_plan = models.JSONField(default=list, blank=True)
    suggestions = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} readiness for {self.target_role}"

