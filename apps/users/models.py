from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=150, default=None)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("first_name",)
    objects = CustomUserManager()
