from rest_framework import mixins, viewsets

from .mixins import DeletionMarkModelMixin


class ListModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class RetrieveUpdateDestroyListModelViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    DeletionMarkModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Override destroy mixin.

    A viewset that provides default `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    pass


class CoreModelViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    DeletionMarkModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    Override destroy mixin.

    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """

    pass
