from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm, UserInfoForm
from .models import UserInfo
from .utils import form_safe_link

admin.site.site_header = "Githance, административная часть"
admin.site.site_title = "Githance"

User = get_user_model()


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    form = UserInfoForm
    can_delete = False
    min_num = 1
    verbose_name = "Дополнительная информация"


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("email", "name", "telegram", "is_staff", "portfolio", "summary")
    search_fields = ("name", "email", "user_info__telegram")
    ordering = ("-pk",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            _("Important dates"),
            {"fields": ("last_login", "date_joined"), "classes": ("collapse",)},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )
    readonly_fields = ("last_login", "date_joined")
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = (UserInfoInline,)
    list_select_related = ("user_info",)

    def save_model(self, request, obj, form, change):
        """Save User and create EmailAddress instance."""
        super().save_model(request, obj, form, change)
        if not change:
            User.objects.create_account_email(user=obj, verified=obj.is_superuser)

    @admin.display(description="Телеграм", ordering="user_info__telegram")
    def telegram(self, obj):
        return obj.user_info.telegram

    @admin.display(description="Портфолио")
    def portfolio(self, obj):
        return form_safe_link(obj.user_info.portfolio_url)

    @admin.display(description="Резюме")
    def summary(self, obj):
        return form_safe_link(obj.user_info.summary_url)
