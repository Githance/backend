from rest_framework import serializers

from apps.users.serializers import UserShortSerializer
from .models import Project


class ProjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "status")
        read_only_fields = fields


class ProjectIntroSerializer(ProjectNameSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "status", "intro")
        read_only_fields = fields


class ProjectDetailSerializer(ProjectIntroSerializer):
    owner = UserShortSerializer(read_only=True, label="Пользователь")

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "intro",
            "description",
            "status",
            "owner",
            "telegram",
            "email",
        )

    def create(self, validated_data):
        return Project.objects.create(
            **validated_data, owner=self.context["request"].user
        )

    def validate_name(self, value):
        """Check constraint for uniqueness violation (owner, name)."""
        action = self.context["view"].action
        if action == "create":
            self._validate_name_create(value)
        if action == "partial_update":
            self._validate_name_update(value)
        return value

    def _validate_name_create(self, value):
        if Project.objects.filter(
            owner=self.context["request"].user, name=value
        ).exists():
            raise serializers.ValidationError("У вас уже есть проект с таким названием")

    def _validate_name_update(self, value):
        if (
            self.instance.name != value
            and Project.objects.filter(owner=self.instance.owner, name=value).exists()
        ):
            raise serializers.ValidationError(
                "У пользователя не может быть двух проектов с одинаковым названием"
            )
