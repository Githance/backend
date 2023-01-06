from .base import *  # noqa: F403,F401

DEBUG = True

# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#access-token-lifetime
SIMPLE_JWT.update(
    {"ACCESS_TOKEN_LIFETIME": timedelta(days=7)},
)
