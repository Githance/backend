from django.contrib import admin

from .models import Participant, Profession, Role

admin.site.register(Participant)
admin.site.register(Profession)
admin.site.register(Role)
