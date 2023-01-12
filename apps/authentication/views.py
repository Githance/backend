from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import SocialLoginView as SocialLoginCallbackView
from dj_rest_auth.views import LoginView
from dj_rest_auth.views import LogoutView as DjRestAuthLogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.http import urlencode
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    LoginAccessTokenSerializer,
    LoginWithPasswordSerializer,
    RefreshAccessTokenSerializer,
)


@extend_schema(exclude=True)
@api_view()
def dummy(request):
    """Do nothing but response 403. Dummy function for dj_rest_auth purposes."""
    return Response(status=status.HTTP_403_FORBIDDEN)


class SocialLoginView(APIView):
    """Redirect the user to the auth server to receive an authorization code."""

    provider = None
    adapter_class = None
    delimiter = " "
    extra_params = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert issubclass(
            self.provider, OAuth2Provider
        ), f"provider is not assigned or incorrect in {self.__class__}."
        assert issubclass(
            self.adapter_class, OAuth2Adapter
        ), f"adapter_class is not assigned or incorrect in {self.__class__} ."

    def get_redirect_url(self):
        url = self.request.build_absolute_uri(reverse(self.provider.id + "_callback"))
        return url

    def get(self, request):
        url = self.adapter_class.authorize_url
        provider = self.provider(request)
        scope = provider.get_scope(request)
        client_id = provider.get_app(request).client_id
        params = {
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": self.get_redirect_url(),
            "scope": self.delimiter.join(set(scope)),
        }
        params.update(self.extra_params)
        url_with_params = "%s?%s" % (url, urlencode(params))
        return HttpResponseRedirect(url_with_params)


@extend_schema(
    responses=LoginAccessTokenSerializer,
    description="Authenticate the user with the Google service (or register first). "
    "Return an access token and put a refresh token in the HttpOnly cookie.",
)
class GoogleLoginView(SocialLoginView):
    """Redirect the user to the Google auth service to receive an authorization code."""

    provider = GoogleProvider
    adapter_class = GoogleOAuth2Adapter
    extra_params = {"prompt": "consent"}


@extend_schema(exclude=True)
class GoogleLoginCallbackView(SocialLoginCallbackView):
    """
    Entry point to the redirected user with an auth code from the Google service.

    Take an authorization code from the redirected user and authenticate the latter
    or register him first. Return an access token.
    """

    allowed_methods = ("GET", "OPTIONS", "HEAD")
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def get(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.query_params)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


RefreshViewWithCookieSupport = get_refresh_view()


class RefreshAccessTokenView(RefreshViewWithCookieSupport):
    """Take the refresh token from the cookie and return the access token."""

    serializer_class = RefreshAccessTokenSerializer


@extend_schema_view(post=extend_schema(responses=LoginAccessTokenSerializer))
class LoginWithPasswordView(LoginView):
    """
    Receive an email and a password, then authenticate the user.

    Return an access token and put a refresh token in the HttpOnly cookie.
    """

    serializer_class = LoginWithPasswordSerializer


# @extend_schema_view(post=extend_schema(responses=RestAuthDetailSerializer))
class LogoutView(DjRestAuthLogoutView):
    """
    Clean up cookies.

    Remove the refresh token and the 'sessionid' (authorization info to the admin site)
    from cookies.
    """

    allowed_methods = ("POST", "OPTIONS", "HEAD")
