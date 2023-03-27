from rest_framework import serializers

from apps.users.serializers import UserShortROSerializer
from .models import Project, ProjectStatus, ProjectType


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ("id", "name")


class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ("id", "name")


class ProjectNameROSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
        label="Статус",
    )

    class Meta:
        model = Project
        fields = ("id", "name", "status")
        read_only_fields = fields


class ProjectIntroROSerializer(ProjectNameROSerializer):
    class Meta:
        model = Project
        fields = ("id", "name", "status", "intro")
        read_only_fields = fields


class ProjectDetailROSerializer(ProjectIntroROSerializer):
    types = ProjectTypeSerializer(many=True, read_only=True, label="Тип проекта")
    owner = UserShortROSerializer(read_only=True, label="Пользователь")

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "intro",
            "description",
            "types",
            "status",
            "owner",
        )
        read_only_fields = fields
