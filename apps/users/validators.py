import re

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator as DjangoEmailValidator


def validate_telegram_name(value):
    regex = re.compile(r"^[a-z][a-z0-9_]{3,30}[a-z0-9]$", flags=re.IGNORECASE)
    if not regex.search(str(value)):
        raise ValidationError(
            "Имя в телеграме может состоять только из английских букв, цифр и _. "
            "Длина от 5 до 32 символов."
        )


class EmailValidator(DjangoEmailValidator):
    # Like the original __call__ , but it doesn't try to convert non-ASCII to punycode.
    def __call__(self, value):
        if not value or "@" not in value:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code, params={"value": value})

        if domain_part not in self.domain_allowlist and not self.validate_domain_part(
            domain_part
        ):
            raise ValidationError(self.message, code=self.code, params={"value": value})
