import re

from django.core.exceptions import ValidationError


def validate_telegram_name(value):
    regex = re.compile(r"^[a-z][a-z0-9_]{3,30}[a-z0-9]$", flags=re.IGNORECASE)
    regex_matches = regex.search(str(value))
    if not regex_matches:
        raise ValidationError(
            "Имя в телеграме должно состоять только из английских букв, "
            "цифр и _. Не может начинаться на цифру и _. Не может заканчиваться _.",
            params={"value": value},
        )
