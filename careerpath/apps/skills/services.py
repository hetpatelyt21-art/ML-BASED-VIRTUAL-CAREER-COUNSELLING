from django.db import transaction

from website.career_resources import get_career_resource

from .models import CareerSkillRequirement, Skill, SkillGapReport, UserSkill


PRIORITY_BY_INDEX = ["high", "high", "medium", "medium", "low"]


def normalize_skill_name(name):
    return " ".join(name.strip().split())


@transaction.atomic
def seed_role_requirements(target_role):
    resource_pack = get_career_resource(target_role)
    requirements = []
    for index, raw_name in enumerate(resource_pack.get("required_skills", [])):
        skill, _ = Skill.objects.get_or_create(name=normalize_skill_name(raw_name))
        requirement, _ = CareerSkillRequirement.objects.update_or_create(
            target_role=target_role,
            skill=skill,
            defaults={
                "required_level": 4 if index < 2 else 3,
                "priority": PRIORITY_BY_INDEX[index] if index < len(PRIORITY_BY_INDEX) else "medium",
            },
        )
        requirements.append(requirement)
    return requirements


@transaction.atomic
def generate_skill_gap_report(assessment_result):
    requirements = seed_role_requirements(assessment_result.career_name)
    user_skill_levels = {
        item.skill_id: item.level
        for item in UserSkill.objects.filter(user=assessment_result.user, skill__in=[req.skill for req in requirements])
    }
    total_required = sum(req.required_level for req in requirements) or 1
    total_current = 0
    missing = []
    priority_plan = []

    for requirement in requirements:
        current_level = user_skill_levels.get(requirement.skill_id, 0)
        total_current += min(current_level, requirement.required_level)
        if current_level < requirement.required_level:
            gap = requirement.required_level - current_level
            item = {
                "skill": requirement.skill.name,
                "current_level": current_level,
                "required_level": requirement.required_level,
                "gap": gap,
                "priority": requirement.priority,
            }
            missing.append(item)
            priority_plan.append({
                **item,
                "next_action": f"Spend two focused weeks building evidence for {requirement.skill.name}.",
            })

    readiness = round((total_current / total_required) * 100)
    suggestions = [
        "Add evidence links for every skill you already know.",
        "Prioritize high-gap, high-priority skills before adding new low-priority skills.",
        "Convert every completed roadmap project into a resume bullet.",
    ]
    return SkillGapReport.objects.update_or_create(
        user=assessment_result.user,
        assessment_result=assessment_result,
        defaults={
            "target_role": assessment_result.career_name,
            "readiness_percentage": readiness,
            "missing_skills": missing,
            "priority_plan": priority_plan,
            "suggestions": suggestions,
        },
    )[0]


def upsert_user_skill(user, skill_name, level, evidence=""):
    skill, _ = Skill.objects.get_or_create(name=normalize_skill_name(skill_name))
    user_skill, _ = UserSkill.objects.update_or_create(
        user=user,
        skill=skill,
        defaults={"level": level, "evidence": evidence},
    )
    return user_skill

