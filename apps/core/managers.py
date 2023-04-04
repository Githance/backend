from django.db import models
from django.shortcuts import get_object_or_404


class VisibleQuerySet(models.QuerySet):
    """
    QuerySet with additional methods, from which you can make a virtual manager.

    In model class:
        objects = VisibleQuerySet.as_manager()
    """

    def visible(self):
        """Return a new QuerySet with only 'visible' (not marked as deleted) objects."""
        return self.filter(deleted_at__isnull=True)

    def get_or_404(self, pk):
        """Return one 'visible' object or raise 404 HTTP error if it doesn't exist."""
        return get_object_or_404(self, pk=pk)
