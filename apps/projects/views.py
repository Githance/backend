from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.core.utils import paginated_response
from apps.participants.models import Participant
from apps.participants.serializers import ParticipantSerializer
from .models import Project, Vacancy
from .permissions import IsOwnerOrReadOnly
from .serializers import ProjectDetailSerializer, ProjectIntroSerializer, VacancySerializer


# TODO uncompleted ProjectViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "patch", "delete", "head", "options")
    lookup_value_regex = r"[0-9]+"

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectIntroSerializer
        if self.action == "participants":
            return ParticipantSerializer
        return ProjectDetailSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return Project.objects.visible().select_related("owner")
        if self.action == "list":
            return (
                Project.objects.visible()
                .select_related("owner")
                .order_by("-last_top_at")
            )
        if self.action == "participants":
            return Participant.objects.visible().select_related(
                "user", "profession", "access_level"
            )
        return Project.objects.visible()

    def get_permissions(self):
        if self.action == "participants":
            return (AllowAny(),)
        return (IsOwnerOrReadOnly(),)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.deleted_at:
            instance.deleted_at = timezone.now()
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @extend_schema(responses=ParticipantSerializer(many=True))
    @action(detail=True)
    def participants(self, request, pk=None, format=None):
        """Return a list of project participants except an owner."""
        Project.objects.visible().get_or_404(pk=pk)
        queryset = self.get_queryset().filter(project__pk=pk)
        return paginated_response(self, queryset, status=status.HTTP_200_OK)


class VacancyViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post", "patch", "delete", "head", "options")
    lookup_value_regex = r"[0-9]+"
    serializer_class = VacancySerializer

