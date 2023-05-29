from rest_framework import serializers

from apps.core.fields import TelegramField
from apps.core.validators import validate_telegram_name
from .models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name")
        read_only_fields = fields


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "telegram",
            "portfolio_url",
            "summary_url",
            "bio",
        )
        read_only_fields = fields


class UserPrivateSerializer(serializers.ModelSerializer):
    telegram = TelegramField(
        allow_blank=True,
        allow_null=True,
        validators=(validate_telegram_name,),
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "telegram",
            "portfolio_url",
            "summary_url",
            "bio",
        )
        extra_kwargs = {
            "email": {"read_only": True},
        }
