from django.urls import path

from . import views

urlpatterns = [
    path("", views.roadmap_dashboard, name="roadmap_dashboard"),
    path("tasks/<int:task_id>/toggle/", views.toggle_task, name="roadmap_task_toggle"),
]
