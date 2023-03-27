from rest_framework import mixins, viewsets


class ListModelViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass
