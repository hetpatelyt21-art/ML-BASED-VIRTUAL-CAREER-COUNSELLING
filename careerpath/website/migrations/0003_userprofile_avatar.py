from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0002_userprofile_avatar_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="avatar",
            field=models.FileField(blank=True, null=True, upload_to="profile_images/"),
        ),
    ]
