from rest_framework import serializers

from .models import AccessLevel, Participant, Profession


class AccessLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessLevel
        fields = ("id", "name")


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ("id", "name")


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ("id", "project", "user", "profession", "access_level")
