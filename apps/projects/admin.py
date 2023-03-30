from django.contrib import admin

from apps.participants.models import Participant
from .models import Project


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ParticipantInline,)
