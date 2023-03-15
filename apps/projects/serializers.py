from rest_framework import serializers

from .models import Project, ProjectStatus, ProjectType


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = ("id", "name")


class ProjectStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatus
        fields = ("id", "name")


class BaseProjectMeta:
    model = Project
    fields = ("id", "name", "status")


class ProjectShortSerializer(serializers.ModelSerializer):
    class Meta(BaseProjectMeta):
        readonly_fields = super().fields


class ProjectListSerializer(ProjectShortSerializer):
    class Meta(BaseProjectMeta):
        fields = super().fields + ("intro",)
        readonly_fields = fields


class ProjectDetailSerializer(ProjectListSerializer):
    # TODO: реализовать сериалайзер
    class Meta(BaseProjectMeta):
        fields = super().fields + (
            "intro",
            "owner",
            "types",
            "description",
            "created_date",
            "last_top_date",
        )
