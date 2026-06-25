from datetime import timedelta
import secrets

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.hashers import check_password, make_password
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar_url = models.URLField(blank=True)
    avatar = models.FileField(upload_to="profile_images/", blank=True, null=True)
    headline = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    interests = models.CharField(max_length=255, blank=True)
    target_role = models.CharField(max_length=120, blank=True)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} profile"


class Feedback(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="feedback_entries"
    )
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback from {self.name}"


class AssessmentResult(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assessment_results"
    )
    domain = models.CharField(max_length=64)
    career_name = models.CharField(max_length=120)
    career_description = models.TextField()
    match_score = models.PositiveIntegerField()
    advanced_score = models.PositiveIntegerField()
    model_confidence = models.PositiveIntegerField()
    salary_text = models.CharField(max_length=120, blank=True)
    outlook_text = models.CharField(max_length=120, blank=True)
    top_traits = models.JSONField(default=list, blank=True)
    top_matches = models.JSONField(default=list, blank=True)
    learning_sources = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.career_name}"


class EmailVerification(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="email_verification"
    )
    otp_hash = models.CharField(max_length=128)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["-created_at"]

    @staticmethod
    def generate_otp():
        return f"{secrets.randbelow(1_000_000):06d}"

    @classmethod
    def create_for_user(cls, user):
        otp = cls.generate_otp()
        verification, _ = cls.objects.update_or_create(
            user=user,
            defaults={
                "otp_hash": make_password(otp),
                "expires_at": timezone.now() + timedelta(minutes=10),
                "verified_at": None,
            },
        )
        return verification, otp

    def is_expired(self):
        return timezone.now() > self.expires_at

    def verify(self, otp):
        if self.verified_at or self.is_expired():
            return False
        if not check_password(otp, self.otp_hash):
            return False
        self.verified_at = timezone.now()
        self.save(update_fields=["verified_at"])
        profile, _ = UserProfile.objects.get_or_create(user=self.user)
        profile.email_verified = True
        profile.save(update_fields=["email_verified"])
        return True

    def __str__(self):
        return f"Email verification for {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    profile, _ = UserProfile.objects.get_or_create(user=instance)
    profile.save()


try:
    from allauth.account.signals import user_signed_up

    @receiver(user_signed_up)
    def mark_social_signup_verified(request, user, **kwargs):
        sociallogin = kwargs.get("sociallogin")
        if sociallogin:
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.email_verified = True
            profile.save(update_fields=["email_verified"])
except ImportError:
    pass
