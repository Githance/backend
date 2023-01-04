from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView as SocialLoginCallbackView
from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.utils.http import urlencode
from django.views import View




from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view()
@permission_classes([IsAuthenticated])
def placeholder(request):
    return Response("ok")


class SocialLoginView(View):
    """
    Redirect the user to the authorization server to receive an authorization code.
    """

    provider = None
    adapter_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        assert self.provider is not None
        assert self.adapter_class is not None

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
            "scope": " ".join(set(scope)),
        }
        url_with_params = "%s?%s" % (url, urlencode(params))
        return HttpResponseRedirect(url_with_params)


class GoogleLoginView(SocialLoginView):
    """
    Redirect the user to the Google auth server to receive an authorization code.
    """

    provider = GoogleProvider
    adapter_class = GoogleOAuth2Adapter


class GoogleLoginCallbackView(SocialLoginCallbackView):
    """
    Entry point to user with authorization code from google server.

    The user can send a POST request with a code in the body or a GET request with a
    code in the query string, depending on your pipeline.
    """

    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

    def get(self, request, *args, **kwargs):
        # Add GET method to retrieve authorization code via query string.
        self.request = request
        self.serializer = self.get_serializer(data=self.request.query_params)
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()
