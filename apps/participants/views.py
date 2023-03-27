from rest_framework.permissions import AllowAny

from apps.core.views import ListModelViewSet
from .models import AccessLevel, Profession
from .serializers import AccessLevelSerializer, ProfessionSerializer


class AccessLevelViewSet(ListModelViewSet):
    """Return a list of all possible access levels."""

    queryset = AccessLevel.objects.all()
    serializer_class = AccessLevelSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class ProfessionViewSet(ListModelViewSet):
    """Return a list of all possible professions."""

    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = (AllowAny,)
