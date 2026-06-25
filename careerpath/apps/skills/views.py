from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import SkillGapReport, UserSkill


@login_required
def skill_gap_dashboard(request):
    report = SkillGapReport.objects.filter(user=request.user).first()
    user_skills = UserSkill.objects.filter(user=request.user).select_related("skill")
    return render(request, "skills/gap_dashboard.html", {"report": report, "user_skills": user_skills})

