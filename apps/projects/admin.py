from django.contrib import admin

from apps.participants.models import Participant
from .models import Project, ProjectStatus, ProjectType, ProjectTypeProject

admin.site.register(ProjectStatus)
admin.site.register(ProjectType)


class ProjectTypeInline(admin.TabularInline):
    model = ProjectTypeProject
    extra = 0


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ParticipantInline, ProjectTypeInline)
