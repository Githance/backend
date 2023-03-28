from django.contrib import admin

from apps.core.admin import BaseChoiceAdmin
from apps.participants.models import Participant
from .models import Project, ProjectStatus, ProjectType, ProjectTypeProject


@admin.register(ProjectStatus)
class ProjectStatusAdmin(BaseChoiceAdmin):
    pass


@admin.register(ProjectType)
class ProjectTypeAdmin(BaseChoiceAdmin):
    pass


class ProjectTypeInline(admin.TabularInline):
    model = ProjectTypeProject
    extra = 0


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ParticipantInline, ProjectTypeInline)
