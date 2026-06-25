from django.db import transaction

from apps.core.learning_engine import recommend_resources
from website.career_resources import get_career_resource

from .models import CareerRoadmap, RoadmapMonth, UserProgress, WeeklyTask


ROLE_BLUEPRINTS = {
    "Software Engineer": [
        ("Programming Foundations", ["Python or JavaScript basics", "Git and GitHub workflow", "Build a CLI mini-project", "Data structures practice"]),
        ("Web Product Skills", ["HTML/CSS/JS fundamentals", "Django or React basics", "Testing and debugging", "Ship a small full-stack app"]),
        ("Career Launch", ["Deployment basics", "Portfolio polish", "Resume optimization", "Internship interview preparation"]),
    ],
    "Data Scientist": [
        ("Data Foundations", ["Python basics", "Statistics fundamentals", "Pandas mini-project", "SQL practice"]),
        ("Machine Learning Practice", ["Model evaluation basics", "Kaggle exercises", "Visualization project", "Feature engineering drills"]),
        ("Deployment and Portfolio", ["Build an end-to-end ML project", "Deploy a notebook-backed demo", "Resume optimization", "Data interview preparation"]),
    ],
    "UI/UX Designer": [
        ("Design Foundations", ["Design principles", "User research basics", "Wireframe a mobile flow", "Figma fundamentals"]),
        ("Product Design Practice", ["Prototype a dashboard", "Run a usability test", "Build a design case study", "Accessibility checklist"]),
        ("Portfolio Launch", ["Polish two case studies", "Create portfolio site", "Resume optimization", "Design interview preparation"]),
    ],
}


def _default_blueprint(target_role, required_skills):
    first_skills = required_skills[:4] or ["career foundations", "communication", "portfolio", "interview practice"]
    return [
        ("Role Foundations", [f"Learn {skill}" for skill in first_skills]),
        ("Applied Practice", ["Complete two guided exercises", "Build a role-specific mini-project", "Collect feedback", "Document your learning"]),
        ("Launch Preparation", ["Complete a portfolio project", "Update resume keywords", "Prepare interview stories", "Apply to five internships or fresher roles"]),
    ]


@transaction.atomic
def generate_roadmap_for_result(assessment_result):
    CareerRoadmap.objects.filter(user=assessment_result.user, is_active=True).update(is_active=False)
    resource_pack = get_career_resource(assessment_result.career_name)
    required_skills = resource_pack.get("required_skills", [])
    blueprint = ROLE_BLUEPRINTS.get(assessment_result.career_name) or _default_blueprint(assessment_result.career_name, required_skills)

    roadmap = CareerRoadmap.objects.create(
        user=assessment_result.user,
        assessment_result=assessment_result,
        target_role=assessment_result.career_name,
        summary=resource_pack.get("roadmap_summary", ""),
        current_level="beginner" if assessment_result.match_score < 70 else "intermediate",
    )
    for month_number, (title, tasks) in enumerate(blueprint, start=1):
        month = RoadmapMonth.objects.create(
            roadmap=roadmap,
            month_number=month_number,
            title=title,
            focus="; ".join(tasks),
        )
        for week_number, task_title in enumerate(tasks, start=1):
            task_type = "project" if "project" in task_title.lower() or "build" in task_title.lower() else "learn"
            if "resume" in task_title.lower():
                task_type = "resume"
            elif "interview" in task_title.lower() or "apply" in task_title.lower():
                task_type = "internship"
            WeeklyTask.objects.create(
                month=month,
                week_number=week_number,
                title=task_title,
                description=_task_description(assessment_result.career_name, task_title),
                task_type=task_type,
            )

    resources = recommend_resources(assessment_result.career_name, required_skills, roadmap.current_level, limit=3)
    for index, item in enumerate(resources[:3], start=1):
        month = roadmap.months.get(month_number=min(index, 3))
        WeeklyTask.objects.create(
            month=month,
            week_number=5,
            title=f"Complete: {item['title']}",
            description=f"{item['provider']} resource for {roadmap.target_role}: {item['url']}",
            task_type="certification" if "Certificate" in item["title"] else "learn",
        )

    progress = UserProgress.objects.create(user=assessment_result.user, roadmap=roadmap)
    progress.recalculate()
    return roadmap


def _task_description(role, title):
    return f"Focus this week on {title.lower()} for your {role} progression path. Capture evidence in your portfolio or resume notes."

