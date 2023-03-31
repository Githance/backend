from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from apps.core.utils import paginated_response
from apps.projects.models import Project
from apps.projects.serializers import ProjectNameSerializer
from .models import User
from .permissions import IsAuthAndIsSelf
from .serializers import UserPrivateSerializer, UserPublicSerializer


@extend_schema_view(
    retrieve=extend_schema(description="Return public information about the user")
)
class UserViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    lookup_value_regex = r"[0-9]+"

    def get_queryset(self):
        if self.action == "projects":
            return Project.objects.all()
        return User.objects.all()

    def get_serializer_class(self):
        if self.action in ("me", "patch_me"):
            return UserPrivateSerializer
        if self.action == "projects":
            return ProjectNameSerializer
        return UserPublicSerializer

    def get_permissions(self):
        if self.action in ("me", "patch_me"):
            return (IsAuthAndIsSelf(),)
        return (AllowAny(),)

    @action(detail=False)
    def me(self, request, format=None):
        """Return public and private information about the current user."""
        instance = get_object_or_404(self.get_queryset(), pk=request.user.pk)
        self.check_object_permissions(self.request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=HTTP_200_OK)

    @me.mapping.patch
    def patch_me(self, request, format=None):
        """Update public and private information about the current user."""
        instance = get_object_or_404(self.get_queryset(), pk=request.user.pk)
        self.check_object_permissions(self.request, instance)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_200_OK)

    @extend_schema(responses=ProjectNameSerializer(many=True))
    @action(detail=True)
    def projects(self, request, pk=None, format=None):
        """Return short information about the user's projects."""
        queryset = (
            self.get_queryset()
            .filter(Q(participants__user__pk=pk) | Q(owner=pk))
            .filter(deleted_at__isnull=True)
            .order_by("-last_top_at")
            .distinct()
        )
        return paginated_response(self, queryset, status=HTTP_200_OK)
