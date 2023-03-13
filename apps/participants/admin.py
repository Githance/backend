from django.contrib import admin

from .models import AccessLevel, Participant, Profession

admin.site.register(Participant)
admin.site.register(Profession)
admin.site.register(AccessLevel)
