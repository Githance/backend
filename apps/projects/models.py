from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.core.models import BaseChoiceModel, BaseModel

User = get_user_model()


class ProjectStatus(BaseChoiceModel):
    class Meta:
        verbose_name = "Статус проекта"
        verbose_name_plural = "Статусы проекта"
        ordering = models.F("order").asc(nulls_last=True), "name"


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
