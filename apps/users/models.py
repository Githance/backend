from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .validators import validate_telegram_name


class UserInfo(models.Model):
    """Additional information to User model."""

    user = models.OneToOneField(
        to="User",
        on_delete=models.CASCADE,
        related_name="user_info",
        verbose_name="Пользователь",
    )
    bio = models.TextField(
        verbose_name="О себе",
        null=True,
        blank=True,
        max_length=1000,
    )
    # telegram username is stored without '@'
    telegram = models.CharField(
        verbose_name="Телеграм",
        null=True,
        blank=True,
        max_length=32,
        validators=[MinLengthValidator(5), validate_telegram_name],
    )
    portfolio_url = models.URLField(
        verbose_name="Ссылка на портфолио",
        null=True,
        blank=True,
    )
    summary_url = models.URLField(
        verbose_name="Ссылка на резюме",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.user.name


class User(AbstractBaseUser, PermissionsMixin):
    from .managers import CustomUserManager

    name = models.CharField("Имя", max_length=38, default=None)
    email = models.EmailField(_("email address"), unique=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("name",)

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return f"{self.name}: {self.email}"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
