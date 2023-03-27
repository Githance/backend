from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.core.models import BaseChoiceModel, BaseModel

User = get_user_model()


class ProjectType(BaseChoiceModel):
    class Meta:
        verbose_name = "Тип проекта"
        verbose_name_plural = "Типы проекта"


class ProjectStatus(BaseChoiceModel):
    class Meta:
        verbose_name = "Статус проекта"
        verbose_name_plural = "Статусы проекта"


class Project(BaseModel):
    name = models.CharField(
        "Название",
        max_length=32,
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        verbose_name="Владелец",
        related_name="own_projects",
    )
    types = models.ManyToManyField(
        ProjectType,
        through="ProjectTypeProject",
        verbose_name="Типы проекта",
        related_name="projects",
    )
    status = models.ForeignKey(
        ProjectStatus,
        on_delete=models.RESTRICT,
        verbose_name="Статус",
        related_name="projects",
    )
    intro = models.CharField(
        "Краткое описание",
        max_length=192,
    )
    description = models.CharField(
        "Подробное описание",
        max_length=2000,
    )
    last_top_at = models.DateTimeField(
        "В топе последний раз",
        default=timezone.now,
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name


class ProjectTypeProject(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name="Проект",
    )
    type = models.ForeignKey(
        ProjectType,
        on_delete=models.RESTRICT,
        verbose_name="Тип проекта",
    )

    class Meta:
        verbose_name = "тип проекта"
        verbose_name_plural = "Типы проекта"
        constraints = [
            models.UniqueConstraint(
                fields=("project", "type"), name="unique_project_type"
            )
        ]
