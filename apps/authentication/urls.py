from dj_rest_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from dj_rest_auth.views import (
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.conf import settings
from django.urls import include, path

from .views import (
    GoogleLoginCallbackView,
    GoogleLoginView,
    LoginWithPasswordView,
    LogoutView,
    RefreshAccessTokenView,
    dummy,
)

main_urls = [
    # dj-rest-auth.registration
    path("registration/", RegisterView.as_view(), name="rest_register"),
    path("verify-email/", VerifyEmailView.as_view(), name="rest_verify_email"),
    path(
        "resend-email/",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
    # dj-rest-auth
    path("login/", LoginWithPasswordView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("token/refresh/", RefreshAccessTokenView.as_view(), name="token_refresh"),
    path("password/reset/", PasswordResetView.as_view(), name="rest_password_reset"),
    path(
        "password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="rest_password_reset_confirm",
    ),
    path("password/change/", PasswordChangeView.as_view(), name="rest_password_change"),
    # dummy
    path(
        "dummy/account-email-verification-sent/",
        dummy,
        name="account_email_verification_sent",
    ),
]

social_urls = [
    path("google/login/", GoogleLoginView.as_view(), name="google_login"),
    path(
        "google/login/callback/",
        GoogleLoginCallbackView.as_view(),
        name="google_callback",
    ),
]

# Dummy URLs for purposes of dj_rest_auth.
# These URLs will be redirected by the web-server to the frontend, but
# here they are needed to automatically generate reverse paths for this.
dummy_front_urls = [
    path(
        settings.FRONTEND_PASS_RESET_CONFIRM_URL + "<uidb64>/<token>/",
        dummy,
        name="password_reset_confirm",
    ),
    path(
        settings.FRONTEND_EMAIL_CONFIRM_URL + "<key>/",
        dummy,
        name="account_confirm_email",
    ),
]


urls = [
    path("", include(main_urls)),
    path("", include(social_urls)),
]

auth_urls = [
    path("auth/", include(urls)),
]

urlpatterns = [
    path("v1/", include(auth_urls)),
]
