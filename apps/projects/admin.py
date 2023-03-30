from django.contrib import admin

from apps.core.admin import BaseChoiceAdmin
from apps.participants.models import Participant
from .models import Project, ProjectStatus


@admin.register(ProjectStatus)
class ProjectStatusAdmin(BaseChoiceAdmin):
    pass


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ParticipantInline,)
