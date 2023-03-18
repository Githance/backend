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
        read_only_fields = BaseProjectMeta.fields


class ProjectListSerializer(ProjectShortSerializer):
    class Meta(BaseProjectMeta):
        fields = BaseProjectMeta.fields + ("intro",)
        read_only_fields = fields


class ProjectDetailSerializer(ProjectListSerializer):
    # TODO: реализовать сериалайзер
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(required=True)
    intro = serializers.CharField(required=True)
    types = ProjectTypeSerializer(many=True)
    description = serializers.CharField(required=True)

    class Meta(BaseProjectMeta):
        fields = BaseProjectMeta.fields + (
            "intro",
            "owner",
            "types",
            "description",
            "created_date",
            "last_top_date",
        )
        read_only_fields = ("created_date", "last_top_date")
