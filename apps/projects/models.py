from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from apps.core.models import BaseModel
from apps.core.validators import EmailValidator, validate_telegram_name

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
    # telegram username is stored without '@'
    telegram = models.CharField(
        verbose_name="Телеграм",
        null=True,
        blank=True,
        max_length=32,
        validators=(MinLengthValidator(5), validate_telegram_name),
    )
    email = models.EmailField(
        verbose_name="Email",
        max_length=254,
        null=True,
        blank=True,
        validators=(EmailValidator(),),
    )
    last_top_at = models.DateTimeField(
        "В топе последний раз",
        default=timezone.now,
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        constraints = [
            models.UniqueConstraint(
                fields=("owner", "name"),
                condition=models.Q(deleted_at__isnull=True),
                name="not_deleted_unique_project",
            )
        ]

    def __str__(self):
        return self.name


class Vacancy(BaseModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        verbose_name="Проект",
        related_name="vacancies",
    )
    profession = models.ForeignKey(
        "participants.Profession",
        on_delete=models.CASCADE,
        verbose_name="Профессия",
        related_name="vacancies",
    )
    description = models.CharField(
        "Подробное описание",
        max_length=2000,
        null=True,
        blank=True,
    )
    is_published = models.BooleanField(
        verbose_name="Опубликована",
    )

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ordering = ("-created_at",)

    def __str__(self):
        return self.profession
