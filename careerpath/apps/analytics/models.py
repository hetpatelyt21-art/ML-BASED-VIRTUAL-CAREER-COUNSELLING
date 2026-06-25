from django.db import models


class WeeklySummary(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name="weekly_summaries")
    week_start = models.DateField()
    roadmap_progress = models.PositiveIntegerField(default=0)
    skills_completed = models.PositiveIntegerField(default=0)
    projects_completed = models.PositiveIntegerField(default=0)
    learning_hours = models.DecimalField(max_digits=6, decimal_places=1, default=0)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "week_start")
        ordering = ["-week_start"]
