from dj_rest_auth.jwt_auth import CookieTokenRefreshSerializer
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DjRestAuthRegisterSerializer,
)
from dj_rest_auth.registration.serializers import (
    SocialLoginSerializer as DjRestAuthSocialLoginSerializer,
)
from dj_rest_auth.serializers import LoginSerializer
from drf_spectacular.utils import extend_schema_serializer
from rest_framework import serializers


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
    name = serializers.CharField(required=True, max_length=38, min_length=1)

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

