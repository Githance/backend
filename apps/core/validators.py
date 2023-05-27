import re

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator as DjangoEmailValidator
from django.utils.regex_helper import _lazy_re_compile


def validate_telegram_name(value):
    regex = re.compile(
        r"^[a-z][a-z0-9_]{3,30}[a-z0-9]$|^@[a-z][a-z0-9_]{4,31}[a-z0-9]$",
        flags=re.IGNORECASE,
    )
    if not regex.search(str(value)):
        raise ValidationError(
            "Имя в телеграме может состоять только из английских букв, цифр и _. "
            "Длина от 5 до 32 символов."
        )


class EmailValidator(DjangoEmailValidator):
    message = "Введите корректный адрес электронной почты"

    # https://github.com/Githance/testing/issues/11
    # Removed %|/! characters to fix sending emails via Beget SMTP server.
    # Removed regex part for quoted string validation.
    user_regex = _lazy_re_compile(
        r"^[-#$&'*+=?^_`{}~0-9A-Z]+(\.[-#$&'*+=?^_`{}~0-9A-Z]+)*\Z",
        re.IGNORECASE,
    )
    # Punycode to exclude.
    punycode = _lazy_re_compile(r"^xn--|\.xn--", re.IGNORECASE)
    forbidden_symbols = _lazy_re_compile(r"[^A-Z0-9-\.]", re.IGNORECASE)

    # https://github.com/Githance/testing/issues/15
    # Like the original __call__ , but it doesn't try to convert non-ASCII to punycode,
    # nor does it accept an existing punycode.
    def __call__(self, value):
        if not value or "@" not in value:
            raise ValidationError(self.message, code=self.code, params={"value": value})

        user_part, domain_part = value.rsplit("@", 1)

        if not self.user_regex.match(user_part):
            raise ValidationError(self.message, code=self.code, params={"value": value})

        if domain_part not in self.domain_allowlist and (
            self.forbidden_symbols.match(domain_part)
            or self.punycode.match(domain_part)
            or not self.validate_domain_part(domain_part)
        ):
            raise ValidationError(self.message, code=self.code, params={"value": value})
