from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name="Время создания",
        auto_now_add=True,
    )
    deleted_at = models.DateTimeField(
        verbose_name="Время удаления",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class BaseChoiceModel(models.Model):
    name = models.CharField(
        "Название",
        max_length=50,
        unique=True,
    )
    order = models.PositiveSmallIntegerField(
        "Порядок отображения",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name
