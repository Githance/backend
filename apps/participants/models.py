from django.db import models

from apps.core.models import BaseChoiceModel, BaseModel
from apps.projects.models import Project, User


class AccessLevel(BaseChoiceModel):
    class Meta:
        verbose_name = "Уровень доступа"
        verbose_name_plural = "Уровни доступа"


class Profession(BaseChoiceModel):
    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"


class Participant(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="participants",
        verbose_name="Проект",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="participants",
        verbose_name="Пользователь",
    )
    access_level = models.ForeignKey(
        AccessLevel,
        on_delete=models.RESTRICT,
        verbose_name="Уровень доступа",
    )
    profession = models.ForeignKey(
        Profession,
        on_delete=models.RESTRICT,
        verbose_name="Профессия",
    )

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

        constraints = [
            models.UniqueConstraint(
                fields=("project", "user", "profession"), name="unique_participant"
            )
        ]

    def __str__(self):
        return f"[{self.user}] [{self.project}] [{self.profession}]"
