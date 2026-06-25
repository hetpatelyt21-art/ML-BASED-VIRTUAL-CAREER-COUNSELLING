from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.roadmap.models import CareerRoadmap
from apps.skills.models import SkillGapReport
from apps.resumes.models import ResumeAnalysis


@login_required
def dashboard(request):
    roadmap = (
        CareerRoadmap.objects.filter(user=request.user, is_active=True)
        .select_related("progress")
        .prefetch_related("months__tasks")
        .first()
    )
    skill_report = SkillGapReport.objects.filter(user=request.user).first()
    resume_analyses = ResumeAnalysis.objects.filter(user=request.user)[:6]
    latest_resume = resume_analyses[0] if resume_analyses else None
    previous_resume = resume_analyses[1] if len(resume_analyses) > 1 else None
    resume_delta = 0
    if latest_resume and previous_resume:
        resume_delta = latest_resume.ats_score - previous_resume.ats_score

    return render(
        request,
        "analytics/dashboard.html",
        {
            "roadmap": roadmap,
            "skill_report": skill_report,
            "latest_resume": latest_resume,
            "resume_delta": resume_delta,
            "resume_analyses": resume_analyses,
        },
    )

