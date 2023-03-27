from django.db.models import F, Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK

from apps.core.utils import paginated_response
from apps.participants.models import Participant
from apps.participants.serializers import ParticipantROSerializer
from .models import Project, ProjectStatus, ProjectType
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    ProjectDetailROSerializer,
    ProjectIntroROSerializer,
    ProjectStatusSerializer,
    ProjectTypeSerializer,
)

SELECTED_PARTICIPANTS_QS = Participant.objects.select_related(
    "user", "profession", "access_level"
)
PREFETCH_PARTICIPANTS = Prefetch("participants", queryset=SELECTED_PARTICIPANTS_QS)


# TODO uncompleted ProjectViewSet
class ProjectViewSet(viewsets.ModelViewSet):
    http_method_names = ("get",)  # temporary
    lookup_value_regex = r"[0-9]+"

    def get_serializer_class(self):
        if self.action == "statuses":
            return ProjectStatusSerializer
        if self.action == "types":
            return ProjectTypeSerializer
        if self.action == "list":
            return ProjectIntroROSerializer
        if self.action == "participants":
            return ParticipantROSerializer
        return ProjectDetailROSerializer

    def get_queryset(self):
        if self.action == "statuses":
            return ProjectStatus.objects.all().order_by(
                F("order").asc(nulls_last=True), "name"
            )
        if self.action == "types":
            return ProjectType.objects.all().order_by(
                F("order").asc(nulls_last=True), "name"
            )
        if self.action == "retrieve":
            return Project.objects.select_related("owner", "status").prefetch_related(
                "types", PREFETCH_PARTICIPANTS
            )
        if self.action == "participants":
            return SELECTED_PARTICIPANTS_QS
        return Project.objects.all()

    def get_permissions(self):
        if self.action in ("statuses", "types", "participants"):
            return (AllowAny(),)
        return (IsOwnerOrReadOnly(),)

    @extend_schema(responses=ProjectStatusSerializer(many=True))
    @action(detail=False, pagination_class=None)
    def statuses(self, format=None):
        """Return a list of all possible project' statuses."""
        return super().list(self.request)

    @extend_schema(responses=ProjectTypeSerializer(many=True))
    @action(detail=False, pagination_class=None)
    def types(self, format=None):
        """Return a list of all possible projects' types."""
        return super().list(self.request)

    @extend_schema(responses=ParticipantROSerializer(many=True))
    @action(detail=True)
    def participants(self, request, pk=None, format=None):
        """Return a list of project participants except an owner."""
        queryset = self.get_queryset().filter(project__pk=pk)
        return paginated_response(self, queryset, status=HTTP_200_OK)
