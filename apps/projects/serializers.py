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
        if Project.objects.filter(
            name=value,
            owner=self.context["request"].user,
        ).exists():
            raise serializers.ValidationError("У вас уже есть проект с таким названием")
        return value
