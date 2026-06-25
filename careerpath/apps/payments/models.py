from django.conf import settings
from django.db import models

from apps.core.models import TimeStampedModel


class Subscription(TimeStampedModel):
    PLAN_CHOICES = [("free", "Free"), ("premium", "Premium"), ("college", "College")]
    PROVIDER_CHOICES = [("razorpay", "Razorpay"), ("stripe", "Stripe"), ("manual", "Manual")]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscription")
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default="free")
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default="manual")
    provider_customer_id = models.CharField(max_length=120, blank=True)
    provider_subscription_id = models.CharField(max_length=120, blank=True)
    active_until = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

