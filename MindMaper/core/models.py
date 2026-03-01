from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BasicTestResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    responses = models.JSONField()
    result = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    EDUCATION_CHOICES = [
        ('highschool', 'High School'),
        ('bachelor', 'Bachelor\'s'),
        ('master', 'Master\'s'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]

    FIELD_CHOICES = [
        ('engineering', 'Engineering'),
        ('medicine', 'Medicine'),
        ('law', 'Law'),
        ('arts', 'Arts'),
        ('commerce', 'Commerce'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(null=True, blank=True)
    education_level = models.CharField(max_length=100, blank=True, null=True)
    preferred_field = models.CharField(max_length=100, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username
