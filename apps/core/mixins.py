from django.utils import timezone
from rest_framework import mixins, status
from rest_framework.response import Response


class DeletionMarkModelMixin(mixins.DestroyModelMixin):
    """Set the deleted_at mark instead of destroying."""

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.deleted_at:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.save()
