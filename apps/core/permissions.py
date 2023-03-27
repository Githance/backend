from rest_framework.permissions import BasePermission


class AllowNobody(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False
