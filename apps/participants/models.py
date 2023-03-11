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
        Project, on_delete=models.CASCADE, related_name="participants"
    )
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="projects")
    role = models.ForeignKey(
        Role,
        on_delete=models.RESTRICT,
    )
    profession = models.ForeignKey(
        Profession,
        on_delete=models.RESTRICT,
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
