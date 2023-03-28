from rest_framework import serializers

from apps.users.serializers import UserShortSerializer
from .models import Project, ProjectStatus, ProjectType


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ("id", "name")


class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ("id", "name")


class ProjectNameSerializer(serializers.ModelSerializer):
    status = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
        label="Статус",
    )

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
    types = ProjectTypeSerializer(many=True, read_only=True, label="Тип проекта")
    owner = UserShortSerializer(read_only=True, label="Пользователь")

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
