from django.contrib import admin

from apps.core.admin import BaseChoiceAdmin
from .models import AccessLevel, Participant, Profession


@admin.register(Profession)
class ProfessionAdmin(BaseChoiceAdmin):
    pass


@admin.register(AccessLevel)
class AccessLevelAdmin(BaseChoiceAdmin):
    pass


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    pass
