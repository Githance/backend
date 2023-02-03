from allauth.account import app_settings as account_settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import (
    DefaultSocialAccountAdapter,
    valid_email_or_none,
)
from allauth.utils import email_address_exists
from rest_framework.exceptions import AuthenticationFailed


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_auto_signup_allowed(self, request, sociallogin):
        # This method has been slightly rewritten to a get rid of the 500 error.
        auto_signup = app_settings.AUTO_SIGNUP
        if auto_signup:
            email = user_email(sociallogin.user)
            if email:
                if account_settings.UNIQUE_EMAIL and email_address_exists(email):
                    # At this point, django-allauth was redirecting to its
                    # 'socialaccount_signup' endpoint, which resulted in NoReverseMatch
                    # error. Now it just says to the user the email is already taken.
                    raise AuthenticationFailed(
                        f"Пользователь с почтой {email} уже существует."
                    )
            elif app_settings.EMAIL_REQUIRED:
                auto_signup = False
        return auto_signup

    def populate_user(self, request, sociallogin, data):
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        name = " ".join((first_name, last_name)).strip()[:38]
        user = sociallogin.user
        user_email(user, valid_email_or_none(email) or "")
        user_field(user, "name", name or "Безымянный")
        return user


class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        email = data.get("email")
        name = data.get("name")[:38]
        user_email(user, valid_email_or_none(email) or "")
        user_field(user, "name", name or "Безымянный")
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user
