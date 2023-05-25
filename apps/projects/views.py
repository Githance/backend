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
from .permissions import (
    CanAddVacancyToProjectOrReadOnly,
    CanEditVacancyOrReadOnly,
    IsProjectOwnerOrReadOnly,
)
from .serializers import (
    ProjectDetailSerializer,
    ProjectIntroSerializer,
    VacancyCreateSerializer,
    VacancySerializer,
)


class ProjectViewSet(CoreModelViewSet):
    """Provide projects API."""

    http_method_names = ("get", "post", "patch", "delete", "head", "options")
    permission_classes = (IsProjectOwnerOrReadOnly,)
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

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    @extend_schema(responses=ParticipantSerializer(many=True))
    @action(detail=True, permission_classes=(AllowAny,))
    def participants(self, request, pk=None):
        """Return a list of project participants except an owner."""
        Project.objects.get_visible_or_404(pk=pk)
        queryset = self.get_queryset().filter(project__pk=pk)
        return paginated_response(self, queryset, status=status.HTTP_200_OK)

    @extend_schema(
        methods=["GET"],
        responses=VacancySerializer(many=True),
        description="Project's vacancies list.",
    )
    @extend_schema(
        methods=["POST"],
        request=VacancyCreateSerializer(),
        responses=VacancySerializer(),
        description="Create new vacancy in project.",
    )
    @action(
        ["get", "post"],
        detail=True,
        permission_classes=(CanAddVacancyToProjectOrReadOnly,),
    )
    def vacancies(self, request, pk):
        project = self.get_object()

        if request.method == "POST":
            serializer = VacancyCreateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            vacancy = serializer.save(project=project)
            serializer = self.get_serializer(instance=vacancy)
            return Response(serializer.data, status=status.HTTP_200_OK)

        queryset = project.vacancies.visible().select_related("project", "profession")
        if request.user != project.owner:
            queryset = queryset.filter(is_published=True)
        return paginated_response(self, queryset, status=status.HTTP_200_OK)


class VacancyViewSet(RetrieveUpdateDestroyListModelViewSet):
    """Provide vacancies API."""

    lookup_value_regex = r"[0-9]+"
    http_method_names = ("get", "patch", "delete", "head", "options")
    serializer_class = VacancySerializer
    permission_classes = (CanEditVacancyOrReadOnly,)
    queryset = Vacancy.objects.visible().select_related("project", "profession")
