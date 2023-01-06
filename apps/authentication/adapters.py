from allauth.account import app_settings as account_settings
from allauth.account.utils import user_email
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
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
