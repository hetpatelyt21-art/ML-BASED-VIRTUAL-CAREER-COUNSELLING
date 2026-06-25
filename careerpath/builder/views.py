from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ResumeEducationForm,
    ResumeExperienceForm,
    ResumeProfileForm,
)
from .models import ResumeEducation, ResumeExperience
from .services import (
    build_resume_docx,
    build_resume_pdf,
    get_or_create_resume_profile,
    resume_filename,
)


@login_required
def resume_edit(request):
    profile = get_or_create_resume_profile(request.user)
    if request.method == "POST":
        form = ResumeProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Resume profile updated.")
            return redirect("resume_preview")
    else:
        form = ResumeProfileForm(instance=profile)
    return render(request, "builder/resume_edit.html", {"form": form, "profile": profile})


@login_required
def resume_preview(request):
    profile = get_or_create_resume_profile(request.user)
    return render(request, "builder/resume_preview.html", {"profile": profile})


@login_required
def resume_download_docx(request):
    profile = get_or_create_resume_profile(request.user)
    return FileResponse(
        build_resume_docx(profile),
        as_attachment=True,
        filename=resume_filename(profile, "docx"),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@login_required
def resume_download_pdf(request):
    profile = get_or_create_resume_profile(request.user)
    return FileResponse(
        build_resume_pdf(profile),
        as_attachment=True,
        filename=resume_filename(profile, "pdf"),
        content_type="application/pdf",
    )


@login_required
def education_add(request):
    profile = get_or_create_resume_profile(request.user)
    if request.method == "POST":
        form = ResumeEducationForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.resume_profile = profile
            item.save()
            messages.success(request, "Education item added.")
            return redirect("resume_preview")
    else:
        form = ResumeEducationForm()
    return render(
        request,
        "builder/resume_item_form.html",
        {"form": form, "item_type": "Education"},
    )


@login_required
def education_edit(request, item_id):
    profile = get_or_create_resume_profile(request.user)
    item = get_object_or_404(ResumeEducation, pk=item_id, resume_profile=profile)
    if request.method == "POST":
        form = ResumeEducationForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Education item updated.")
            return redirect("resume_preview")
    else:
        form = ResumeEducationForm(instance=item)
    return render(
        request,
        "builder/resume_item_form.html",
        {"form": form, "item_type": "Education"},
    )


@login_required
def experience_add(request):
    profile = get_or_create_resume_profile(request.user)
    if request.method == "POST":
        form = ResumeExperienceForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.resume_profile = profile
            item.save()
            messages.success(request, "Experience item added.")
            return redirect("resume_preview")
    else:
        form = ResumeExperienceForm()
    return render(
        request,
        "builder/resume_item_form.html",
        {"form": form, "item_type": "Experience"},
    )


@login_required
def experience_edit(request, item_id):
    profile = get_or_create_resume_profile(request.user)
    item = get_object_or_404(ResumeExperience, pk=item_id, resume_profile=profile)
    if request.method == "POST":
        form = ResumeExperienceForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience item updated.")
            return redirect("resume_preview")
    else:
        form = ResumeExperienceForm(instance=item)
    return render(
        request,
        "builder/resume_item_form.html",
        {"form": form, "item_type": "Experience"},
    )
