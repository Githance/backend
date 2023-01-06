from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView as SocialLoginCallbackView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.http import urlencode
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def dummy(request):
    """Do nothing but response 403. Dummy function for dj_rest_auth purposes."""
    return Response(status=status.HTTP_403_FORBIDDEN)


class SocialLoginView(View):
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


class GoogleLoginView(SocialLoginView):
    """Redirect the user to the Google auth server to receive an authorization code."""

    provider = GoogleProvider
    adapter_class = GoogleOAuth2Adapter
    extra_params = {"prompt": "consent"}


class GoogleLoginCallbackView(SocialLoginCallbackView):
    """
    Entry point to user with authorization code from google server.

    The user can send a POST request with a code in the body or a GET request with a
    code in the query string, depending on your pipeline.
    """

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    # Add GET method to receive authorization code via query string.
    def get(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=self.request.query_params)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()
