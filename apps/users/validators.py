import re

from django.core.exceptions import ValidationError


def validate_telegram_name(value):
    regex = re.compile(r"^[a-z][a-z0-9_]{3,30}[a-z0-9]$", flags=re.IGNORECASE)
    if not regex.search(str(value)):
        raise ValidationError(
            "Имя в телеграме может состоять только из английских букв, цифр и _. "
            "Длина от 5 до 32 символов."
        )
