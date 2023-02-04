from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import (
    SocialLoginView as DjRestAuthSocialLoginView,
)
from dj_rest_auth.views import LoginView
from dj_rest_auth.views import LogoutView as DjRestAuthLogoutView
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    LoginAccessTokenSerializer,
    LoginWithPasswordSerializer,
    RefreshAccessTokenSerializer,
    SocialLoginSerializer,
)


@extend_schema(exclude=True)
@api_view()
def dummy(request):
    """Do nothing but response 403. Dummy function for dj_rest_auth purposes."""
    return Response(status=status.HTTP_403_FORBIDDEN)


@extend_schema(responses=LoginAccessTokenSerializer)
class GoogleLoginView(DjRestAuthSocialLoginView):
    """
    Entry point to the user with the Google service authentication code.

    Take 'code' from the user, authenticate the latter or register him first.
    Return 'access_token' and put 'ref_token' and 'sessionid' in the HttpOnly cookie.
    """

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer


RefreshViewWithCookieSupport = get_refresh_view()


class RefreshAccessTokenView(RefreshViewWithCookieSupport):
    """Take the refresh token from the cookie and return the access token."""

    serializer_class = RefreshAccessTokenSerializer


@extend_schema(responses=LoginAccessTokenSerializer)
class LoginWithPasswordView(LoginView):
    """
    Receive 'email' and 'password', then authenticate the user.

    Return 'access_token' and put a 'ref_token' in the HttpOnly cookie.
    """

    serializer_class = LoginWithPasswordSerializer


class LogoutView(DjRestAuthLogoutView):
    """
    Clean up cookies.

    Remove 'ref_token' and 'sessionid' (authorization data for logging into the site
    admin panel) from cookies.
    """

    allowed_methods = ("POST", "OPTIONS", "HEAD")
