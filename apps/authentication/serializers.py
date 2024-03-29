from dj_rest_auth.jwt_auth import CookieTokenRefreshSerializer
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DjRestAuthRegisterSerializer,
)
from dj_rest_auth.registration.serializers import (
    SocialLoginSerializer as DjRestAuthSocialLoginSerializer,
)
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import settings
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers

from apps.core.validators import EmailValidator


class LoginAccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()


@extend_schema_serializer(exclude_fields=("refresh",))
class RefreshAccessTokenSerializer(CookieTokenRefreshSerializer):
    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs.pop("refresh", None)
        return attrs


class RegisterSerializer(DjRestAuthRegisterSerializer):
    username = None
    name = serializers.CharField(
        required=True,
        max_length=38,
        min_length=1,
    )
    email = serializers.CharField(
        required=True,
        max_length=254,
        validators=(EmailValidator(),),
    )

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({"name": self.validated_data.get("name", "")})
        return data


class LoginWithPasswordSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)


class SocialLoginSerializer(DjRestAuthSocialLoginSerializer):
    access_token = None
    id_token = None
    code = serializers.CharField()

    def set_callback_url(self, view, adapter_class):
        origin = view.request.META.get("HTTP_ORIGIN", "")
        is_allow_localhost = settings.ALLOW_GOOGLE_CODE_FROM_LOCALHOST_3000

        if origin and origin != "http://localhost:3000":
            self.callback_url = origin + "/" + settings.FRONTEND_GOOGLE_CALLBACK_URL
        elif origin == "http://localhost:3000" and is_allow_localhost:
            self.callback_url = (
                "http://localhost:3000/" + settings.FRONTEND_GOOGLE_CALLBACK_URL
            )
        else:
            super().set_callback_url(view, adapter_class)
