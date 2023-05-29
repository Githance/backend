from rest_framework.fields import CharField


class TelegramField(CharField):
    def __init__(self, **kwargs):
        kwargs["label"] = kwargs.get("label", "Телеграм")
        super().__init__(**kwargs)

    def to_internal_value(self, value):
        value = super().to_internal_value(value)
        if not value.startswith("@"):
            value = "@" + value
        return value
