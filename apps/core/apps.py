from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig as DjangoAdminConfig
from django.contrib.auth.apps import AuthConfig as DjangoAuthConfig


class AdminConfig(DjangoAdminConfig):
    default_site = "apps.core.admin.AdminSite"


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"


class AuthConfig(DjangoAuthConfig):
    verbose_name = "Права в админке"
