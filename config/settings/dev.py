from corsheaders.defaults import default_headers

from .base import *  # noqa: F403,F401

DEBUG = True

SIMPLE_JWT.update(
    {
        "ACCESS_TOKEN_LIFETIME": timedelta(
            minutes=env.int("DJANGO_ACCESS_TOKEN_LIFETIME", 60 * 24 * 7)
        )
    }
)

# Allow setting cookie on http:// from https:// server
CORS_ALLOW_HEADERS = [*default_headers, "credentials"]
CORS_ALLOW_CREDENTIALS = True
JWT_AUTH_SAMESITE = "None"
JWT_AUTH_SECURE = False


# -------------------------------- DJANGO DEBUG TOOLBAR --------------------------------

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#prerequisites
INSTALLED_APPS += ["debug_toolbar"]
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
# https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
DEBUG_TOOLBAR_CONFIG = {
    "TOOLBAR_LANGUAGE": "en-us",
    "SHOW_COLLAPSED": True,
    "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG and request.user.is_staff,
}
