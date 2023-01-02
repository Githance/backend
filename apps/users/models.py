from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    username = None
    USERNAME_FIELD = "email"
    email = models.EmailField(_("email address"), unique=True)
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
