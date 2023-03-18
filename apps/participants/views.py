from rest_framework import viewsets

from .models import AccessLevel, Participant, Profession
from .serializers import (
    AccessLevelSerializer,
    ParticipantSerializer,
    ProfessionSerializer,
)


class AccessLevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccessLevel.objects.all()
    serializer_class = AccessLevelSerializer


class ParticipantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class ProfessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
