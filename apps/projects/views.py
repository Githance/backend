from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK

from apps.core.utils import paginated_response
from apps.participants.models import Participant
from apps.participants.serializers import ParticipantSerializer
from .models import Project
from .permissions import IsOwnerOrReadOnly
from .serializers import ProjectDetailSerializer, ProjectIntroSerializer


# TODO uncompleted ProjectViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post")  # temporary
    lookup_value_regex = r"[0-9]+"

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectIntroSerializer
        if self.action == "participants":
            return ParticipantSerializer
        return ProjectDetailSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return Project.objects.select_related("owner")
        if self.action == "participants":
            return Participant.objects.select_related(
                "user", "profession", "access_level"
            )
        return Project.objects.all()

    def get_permissions(self):
        if self.action == "participants":
            return (AllowAny(),)
        return (IsOwnerOrReadOnly(),)

    @extend_schema(responses=ParticipantSerializer(many=True))
    @action(detail=True)
    def participants(self, request, pk=None, format=None):
        """Return a list of project participants except an owner."""
        queryset = self.get_queryset().filter(project__pk=pk)
        return paginated_response(self, queryset, status=HTTP_200_OK)
