from django.urls import path

from . import views

urlpatterns = [
    path("analyzer/", views.resume_analyzer, name="resume_analyzer"),
]
