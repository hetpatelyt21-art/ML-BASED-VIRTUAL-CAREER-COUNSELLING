from django.contrib import admin

from .models import AssessmentResult, Feedback, UserProfile


Feedback._meta.verbose_name = "Message"
Feedback._meta.verbose_name_plural = "Messages"


@admin.register(Feedback)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender_name", "account_username", "message_preview", "created_at")
    search_fields = ("name", "email", "message", "user__username")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("user", "name", "email", "message", "created_at")

    @admin.display(description="Name")
    def sender_name(self, obj):
        return obj.name

    @admin.display(description="Username")
    def account_username(self, obj):
        return obj.user.username if obj.user else "-"

    @admin.display(description="Message")
    def message_preview(self, obj):
        preview = obj.message.strip()
        if len(preview) <= 80:
            return preview
        return f"{preview[:77]}..."


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ("user", "career_name", "domain", "match_score", "created_at")
    search_fields = ("user__username", "career_name", "domain")
    list_filter = ("domain", "created_at")
    ordering = ("-created_at",)
