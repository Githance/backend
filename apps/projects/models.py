from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel

User = get_user_model()


class Project(BaseModel):
    class Status(models.TextChoices):
        IDEA = ("idea", "идея")
        VACANCY = ("vacancy", "идет набор")
        IN_PROGRESS = ("in_progress", "в процессе")
        CLOSED = ("closed", "закрыт")

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
    status = models.CharField(
        choices=Status.choices,
        verbose_name="Статус",
        max_length=20,
        default=Status.IDEA,
    )
    intro = models.CharField(
        "Краткое описание",
        max_length=192,
    )
    description = models.CharField(
        "Подробное описание",
        max_length=2000,
        null=True,
        blank=True,
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
