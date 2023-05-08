from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly

from apps.participants.models import Participant


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.owner == request.user


class IsProjectOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.project.owner == request.user


class IsVacancyEditor(IsProjectOwnerOrReadOnly):
    def has_object_permission(self, request, view, obj):
        if super().has_object_permission(request, view, obj):
            return True
        queryset = Participant.objects.visible().select_related("access_level")
        queryset = queryset.filter(
            user=request.user,
            project=obj.project,
            access_level__vacancy_editing=True,
        )
        return queryset.exists()
