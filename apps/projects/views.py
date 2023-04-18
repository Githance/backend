from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.core.utils import paginated_response
from apps.core.views import CoreModelViewSet, RetrieveUpdateDestroyListModelViewSet
from apps.participants.models import Participant
from apps.participants.serializers import ParticipantSerializer
from .models import Project, Vacancy
from .permissions import IsOwnerOrReadOnly, IsProjectOwnerOrReadOnly
from .serializers import (
    ProjectDetailSerializer,
    ProjectIntroSerializer,
    VacancySerializer,
)


# TODO uncompleted ProjectViewSet
class ProjectViewSet(CoreModelViewSet):
    http_method_names = ("get", "post", "patch", "delete", "head", "options")
    lookup_value_regex = r"[0-9]+"
    serializers_map = {
        "list": ProjectIntroSerializer,
        "participants": ParticipantSerializer,
        "vacancies": VacancySerializer,
    }

    def get_serializer_class(self):
        if self.action in ProjectViewSet.serializers_map:
            return ProjectViewSet.serializers_map[self.action]
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

    @extend_schema(responses=ParticipantSerializer(many=True))
    @action(detail=True)
    def participants(self, request, pk=None, format=None):
        """Return a list of project participants except an owner."""
        Project.objects.visible().get_or_404(pk=pk)
        queryset = self.get_queryset().filter(project__pk=pk)
        return paginated_response(self, queryset, status=status.HTTP_200_OK)

    @extend_schema(responses=VacancySerializer(many=True))
    @action(["get", "post"], detail=True)
    def vacancies(self, request, pk):
        project = Project.objects.visible().get_or_404(pk=pk)

        if request.method == "POST":
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = project.vacancies.visible().select_related("project", "profession")
        return paginated_response(self, queryset, status=status.HTTP_200_OK)


class VacancyViewSet(RetrieveUpdateDestroyListModelViewSet):
    lookup_value_regex = r"[0-9]+"
    http_method_names = ("get", "post", "patch", "delete", "head", "options")
    serializer_class = VacancySerializer
    permission_classes = (IsProjectOwnerOrReadOnly,)
    queryset = Vacancy.objects.visible().select_related("project", "profession")
