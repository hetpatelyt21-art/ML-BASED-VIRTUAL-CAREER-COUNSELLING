from django.urls import path

from . import views

urlpatterns = [
    path("", views.skill_gap_dashboard, name="skill_gap_dashboard"),
]
