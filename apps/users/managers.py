from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db import transaction


class CustomUserManager(UserManager):
    def create_account_email(self, user, verified=False):
        from allauth.account.models import EmailAddress

        EmailAddress.objects.create(
            user=user,
            email=user.email,
            verified=verified,
            primary=True,
        )

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)

        with transaction.atomic():
            user.save(using=self._db)
            self.create_account_email(user, verified=user.is_superuser)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
