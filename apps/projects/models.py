from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class AbstractClassifier(models.Model):
    """Abstract model for standard classifier."""

    name = models.CharField("Название", max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ProjectType(AbstractClassifier):
    class Meta:
        verbose_name = "Тип проекта"
        verbose_name_plural = "Типы проекта"


class ProjectStatus(AbstractClassifier):
    class Meta:
        verbose_name = "Статус проекта"
        verbose_name_plural = "Статусы проекта"


class Project(AbstractClassifier):
    owner = models.ForeignKey(
        User,
        on_delete=models.RESTRICT,
        verbose_name="Владелец",
        related_name="own_projects",
    )
    types = models.ManyToManyField(
        ProjectType,
        verbose_name="Типы проекта",
    )
    status = models.ForeignKey(
        ProjectStatus,
        on_delete=models.RESTRICT,
        verbose_name="Статус",
    )
    intro = models.CharField(
        "Краткое описание",
        max_length=192,
    )
    description = models.CharField(
        "Подробное описание",
        max_length=2000,
    )
    created_date = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )
    last_top_date = models.DateTimeField(
        "Дата последнего события",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
