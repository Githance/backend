from django.db import models

from apps.projects.models import AbstractClassifier, Project, User


class AccessLevel(AbstractClassifier):
    class Meta:
        verbose_name = "Уровень доступа"
        verbose_name_plural = "Уровни доступа"


class Profession(AbstractClassifier):
    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"


class Participant(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="participants",
        verbose_name="Проект",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        related_name="projects",
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
    join_date = models.DateTimeField(
        "Дата присоединения",
        auto_now_add=True,
    )
    leave_date = models.DateTimeField(
        "Дата прекращения участия",
        null=True,
        blank=True,
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
        return f"[{self.user}][{self.project}][{self.profession}]"
