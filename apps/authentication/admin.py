from allauth.socialaccount.models import SocialApp, SocialToken
from django.contrib import admin

# Hide unusable app installed by django-allauth.
# 'allauth.socialaccount' must be higher than 'app.authentication' in INSTALLED_APPS.
admin.site.unregister(SocialToken)
admin.site.unregister(SocialApp)
