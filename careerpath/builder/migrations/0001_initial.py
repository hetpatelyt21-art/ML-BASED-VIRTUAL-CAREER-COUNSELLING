from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ResumeProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("headline", models.CharField(blank=True, max_length=160)),
                ("summary", models.TextField(blank=True)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("phone", models.CharField(blank=True, max_length=30)),
                ("linkedin_url", models.URLField(blank=True)),
                ("github_url", models.URLField(blank=True)),
                ("portfolio_url", models.URLField(blank=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="resume_profile", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="PortfolioProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("description", models.TextField()),
                ("project_url", models.URLField(blank=True)),
                ("repo_url", models.URLField(blank=True)),
                ("skills_text", models.CharField(blank=True, max_length=255)),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="portfolio_projects", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-is_featured", "-created_at"]},
        ),
        migrations.CreateModel(
            name="ResumeExperience",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("organization", models.CharField(max_length=160)),
                ("start_date", models.DateField()),
                ("end_date", models.DateField(blank=True, null=True)),
                ("description", models.TextField(blank=True)),
                ("resume_profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="experience_items", to="builder.resumeprofile")),
            ],
            options={"ordering": ["-start_date", "-id"]},
        ),
        migrations.CreateModel(
            name="ResumeEducation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("institution", models.CharField(max_length=160)),
                ("degree", models.CharField(max_length=160)),
                ("start_year", models.PositiveIntegerField()),
                ("end_year", models.PositiveIntegerField(blank=True, null=True)),
                ("description", models.TextField(blank=True)),
                ("resume_profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="education_items", to="builder.resumeprofile")),
            ],
            options={"ordering": ["-start_year", "-id"]},
        ),
    ]
