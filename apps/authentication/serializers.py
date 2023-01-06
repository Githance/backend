from rest_framework import serializers


class LoginJWTSerializer(serializers.Serializer):
    # Removed redundant fields (refresh_token and user) from default JWTSerializer.
    access_token = serializers.CharField()
