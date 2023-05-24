from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly

from apps.participants.models import Participant


class ProjectPermission:
    def __init__(self, project, permissions=None):
        self._project = project
        if permissions:
            self._permissions_kwargs = {
                "access_level__" + permit: True for permit in permissions
            }

    def is_project_owner(self, user):
        return self._project.owner == user

    def has_access(self, user):
        if self.is_project_owner(user):
            return True
        if not hasattr(self, "_permissions_kwargs"):
            return False
        queryset = Participant.objects.visible().select_related("access_level")
        queryset = queryset.filter(
            user=user,
            project=self._project,
            **self._permissions_kwargs,
        )
        return queryset.exists()


class IsProjectOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, project):
        if request.method in SAFE_METHODS:
            return True
        return ProjectPermission(project).is_project_owner(request.user)


class CanAddVacancyToProjectOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, project):
        if request.method in SAFE_METHODS:
            return True
        return ProjectPermission(
            project=project,
            permissions=("can_edit_vacancy",),
        ).has_access(request.user)


class CanEditVacancyOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, vacancy):
        if request.method in SAFE_METHODS:
            return True
        return ProjectPermission(
            project=vacancy.project,
            permissions=("can_edit_vacancy",),
        ).has_access(request.user)
