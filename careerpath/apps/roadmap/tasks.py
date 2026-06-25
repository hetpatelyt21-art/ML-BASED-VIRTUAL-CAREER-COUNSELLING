from django.core.mail import send_mail
from django.conf import settings

try:
    from careerpath.celery import app
except ImportError:
    app = None


def _send_roadmap_reminder(user_email, task_title):
    send_mail(
        "Your Mentoraa roadmap reminder",
        f"Keep your progression moving: {task_title}",
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=True,
    )


if app:
    roadmap_reminder = app.task(_send_roadmap_reminder, name="roadmap.reminder")
else:
    roadmap_reminder = _send_roadmap_reminder
