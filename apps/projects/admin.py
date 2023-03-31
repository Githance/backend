from django.contrib import admin

from apps.participants.models import Participant
from .forms import ProjectModelForm
from .models import Project


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "profession",
                    "access_level",
                    "created_at",
                    "deleted_at",
                )
            },
        ),
    )
    readonly_fields = ("created_at", "deleted_at")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectModelForm

    list_display = (
        "id",
        "name",
        "last_top_at",
        "status",
        "owner",
        "telegram",
        "email",
        "created_at",
        "deleted_at",
    )
    list_display_links = (
        "id",
        "name",
    )
    search_fields = ("name", "owner", "email", "telegram")
    ordering = ("-last_top_at",)
    list_filter = ("status", "created_at", "deleted_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "owner",
                    "intro",
                    "description",
                    "status",
                )
            },
        ),
        (
            "Контакты",
            {
                "fields": (
                    "telegram",
                    "email",
                ),
            },
        ),
        (
            "Даты",
            {
                "fields": (
                    "created_at",
                    "last_top_at",
                    "deleted_at",
                ),
            },
        ),
    )
    readonly_fields = ("created_at", "status")
    inlines = (ParticipantInline,)
