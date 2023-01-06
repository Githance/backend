from allauth.socialaccount.models import SocialToken
from django.contrib import admin

# Hide unusable app installed by django-allauth.
admin.site.unregister(SocialToken)
