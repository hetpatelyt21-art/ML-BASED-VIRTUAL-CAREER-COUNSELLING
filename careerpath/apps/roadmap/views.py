from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import CareerRoadmap, WeeklyTask


@login_required
def roadmap_dashboard(request):
    roadmap = (
        CareerRoadmap.objects.filter(user=request.user, is_active=True)
        .prefetch_related("months__tasks")
        .select_related("progress")
        .first()
    )
    return render(request, "roadmap/dashboard.html", {"roadmap": roadmap})


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(WeeklyTask, pk=task_id, month__roadmap__user=request.user)
    task.completed = not task.completed
    task.completed_at = timezone.now() if task.completed else None
    task.save(update_fields=["completed", "completed_at", "updated_at"])
    task.month.roadmap.progress.recalculate()
    messages.success(request, "Roadmap progress updated.")
    return redirect("roadmap_dashboard")

