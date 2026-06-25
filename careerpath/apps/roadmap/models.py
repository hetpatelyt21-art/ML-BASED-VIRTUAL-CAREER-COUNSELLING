from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class CareerRoadmap(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="career_roadmaps")
    assessment_result = models.OneToOneField(
        "website.AssessmentResult",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="career_roadmap",
    )
    target_role = models.CharField(max_length=140)
    summary = models.TextField(blank=True)
    current_level = models.CharField(max_length=32, default="beginner")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} -> {self.target_role}"

    @property
    def completion_percentage(self):
        progress = getattr(self, "progress", None)
        if progress:
            return progress.completion_percentage
        total = WeeklyTask.objects.filter(month__roadmap=self).count()
        done = WeeklyTask.objects.filter(month__roadmap=self, completed=True).count()
        return round((done / total) * 100) if total else 0


class RoadmapMonth(models.Model):
    roadmap = models.ForeignKey(CareerRoadmap, on_delete=models.CASCADE, related_name="months")
    month_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=160)
    focus = models.TextField()

    class Meta:
        ordering = ["month_number"]
        unique_together = ("roadmap", "month_number")

    def __str__(self):
        return f"Month {self.month_number}: {self.title}"

    @property
    def completion_percentage(self):
        tasks = list(self.tasks.all())
        if not tasks:
            return 0
        completed = sum(1 for task in tasks if task.completed)
        return round((completed / len(tasks)) * 100)


class WeeklyTask(TimeStampedModel):
    TASK_TYPES = [
        ("learn", "Learning"),
        ("project", "Project"),
        ("certification", "Certification"),
        ("internship", "Internship Prep"),
        ("resume", "Resume"),
    ]

    month = models.ForeignKey(RoadmapMonth, on_delete=models.CASCADE, related_name="tasks")
    week_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=24, choices=TASK_TYPES, default="learn")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["month__month_number", "week_number", "id"]

    def __str__(self):
        return self.title


class UserProgress(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="roadmap_progress")
    roadmap = models.OneToOneField(CareerRoadmap, on_delete=models.CASCADE, related_name="progress")
    completed_tasks = models.PositiveIntegerField(default=0)
    total_tasks = models.PositiveIntegerField(default=0)
    completion_percentage = models.PositiveIntegerField(default=0)
    learning_hours = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "User progress"

    def recalculate(self):
        tasks = WeeklyTask.objects.filter(month__roadmap=self.roadmap)
        self.total_tasks = tasks.count()
        self.completed_tasks = tasks.filter(completed=True).count()
        self.projects_completed = tasks.filter(task_type="project", completed=True).count()
        self.completion_percentage = round((self.completed_tasks / self.total_tasks) * 100) if self.total_tasks else 0
        self.save(update_fields=["total_tasks", "completed_tasks", "projects_completed", "completion_percentage", "updated_at"])
        return self

