from rest_framework import status, viewsets

from .models import Project, ProjectStatus, ProjectType
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import (
    ProjectDetailSerializer,
    ProjectListSerializer,
    ProjectShortSerializer,
    ProjectStatusSerializer,
    ProjectTypeSerializer,
)


class ProjectTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


class ProjectStatusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectStatus.objects.all()
    serializer_class = ProjectStatusSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = (IsOwnerOrStaffOrReadOnly,)

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        # TODO: Оптимизация запросов
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        pass
        # TODO: set deleted
