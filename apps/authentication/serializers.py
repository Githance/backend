from dj_rest_auth.jwt_auth import CookieTokenRefreshSerializer
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DjRestAuthRegisterSerializer,
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
    first_name = serializers.CharField(required=True, max_length=150, min_length=1)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({"first_name": self.validated_data.get("first_name", "")})
        return data


class LoginWithPasswordSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
