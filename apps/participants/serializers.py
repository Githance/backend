from rest_framework import serializers

from .models import AccessLevel, Participant, Profession


class AccessLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLevel
        fields = ("id", "name")


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ("id", "name")


class ParticipantSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        read_only=True,
        label="Идентификатор пользователя",
    )
    name = serializers.CharField(
        source="user.name",
        label="Имя пользователя",
    )
    profession = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
        label="Профессия в проекте",
    )
    access_level = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
        label="Полномочия в проекте",
    )

    class Meta:
        model = Participant
        fields = ("user_id", "name", "profession", "access_level")
        read_only_fields = fields
