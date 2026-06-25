from django.urls import path

from . import views

urlpatterns = [
    path("resume/", views.resume_edit, name="resume_edit"),
    path("resume/preview/", views.resume_preview, name="resume_preview"),
    path("resume/download/docx/", views.resume_download_docx, name="resume_download_docx"),
    path("resume/download/pdf/", views.resume_download_pdf, name="resume_download_pdf"),
    path("resume/education/add/", views.education_add, name="education_add"),
    path("resume/education/<int:item_id>/edit/", views.education_edit, name="education_edit"),
    path("resume/experience/add/", views.experience_add, name="experience_add"),
    path("resume/experience/<int:item_id>/edit/", views.experience_edit, name="experience_edit"),
]
