from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly

from apps.participants.models import Participant
from apps.projects.models import Project


class ProjectPermission:
    def _get_project(self, obj):
        if isinstance(obj, Project):
            return obj
        return getattr(obj, "project", None)

    def _is_project_owner(self, user, obj):
        project = self._get_project(obj)
        return bool(project and project.owner == user)

    def _check_access_level(self, user, obj, permissions):
        project = self._get_project(obj)
        if project is None:
            return False

        permissions_kwargs = {"access_level__" + permit: True for permit in permissions}
        queryset = Participant.objects.visible().select_related("access_level")
        queryset = queryset.filter(
            user=user,
            project=project,
            **permissions_kwargs,
        )
        return queryset.exists()


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly, ProjectPermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return self._is_project_owner(request.user, obj)


class IsVacancyEditorOrReadOnly(IsAuthenticatedOrReadOnly, ProjectPermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if self._is_project_owner(request.user, obj):
            return True
        return self._check_access_level(request.user, obj, ("vacancy_editing",))
