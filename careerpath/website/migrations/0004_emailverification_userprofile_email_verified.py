import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def ensure_existing_profiles(apps, schema_editor):
    User = apps.get_model("auth", "User")
    UserProfile = apps.get_model("website", "UserProfile")
    for user in User.objects.all():
        UserProfile.objects.get_or_create(
            user=user,
            defaults={"email_verified": True},
        )
    UserProfile.objects.update(email_verified=True)


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0003_userprofile_avatar"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="email_verified",
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name="EmailVerification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("otp_hash", models.CharField(max_length=128)),
                ("expires_at", models.DateTimeField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("verified_at", models.DateTimeField(blank=True, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_verification",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.RunPython(ensure_existing_profiles, migrations.RunPython.noop),
    ]
