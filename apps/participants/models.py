from django.db import models

from apps.projects.models import AbstractClassifier, Project, User


class Role(AbstractClassifier):
    class Meta:
        verbose_name = "Проектная роль"
        verbose_name_plural = "Проектные роли"


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
        verbose_name="Участник",
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
        verbose_name="Роль",
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
        return f"{self.user} участвует в {self.project} как {self.profession}"
