from apps.resumes.models import ResumeAnalysis
from apps.roadmap.models import CareerRoadmap
from apps.skills.models import SkillGapReport

from .providers import get_ai_provider


def build_user_context(user):
    latest_result = user.assessment_results.first()
    roadmap = CareerRoadmap.objects.filter(user=user, is_active=True).select_related("progress").first()
    skill_report = SkillGapReport.objects.filter(user=user).first()
    resume = ResumeAnalysis.objects.filter(user=user).first()
    return {
        "target_role": latest_result.career_name if latest_result else "",
        "assessment_match": latest_result.match_score if latest_result else None,
        "roadmap_progress": roadmap.progress.completion_percentage if roadmap and hasattr(roadmap, "progress") else 0,
        "readiness": skill_report.readiness_percentage if skill_report else 0,
        "missing_skills": skill_report.missing_skills if skill_report else [],
        "resume_score": resume.ats_score if resume else None,
    }


def mentor_reply(user, prompt, provider_name=None):
    context = build_user_context(user)
    provider = get_ai_provider(provider_name)
    messages = [
        {
            "role": "system",
            "content": (
                "You are Mentoraa's career progression mentor. Use the user's assessment, roadmap, "
                "skill gaps, and resume score. Give specific next actions, not generic motivation. "
                f"User context: {context}"
            ),
        },
        {"role": "user", "content": prompt},
    ]
    return provider.complete(messages)
