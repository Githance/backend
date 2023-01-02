from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


# https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key
SECRET_KEY = env.str(
    "DJANGO_SECRET_KEY",
    "django-insecure-#4!pz=idpegh$47_#ry6^@6xf!osm0^=_c63u2rf+5k)nsd16i",
)

# https://docs.djangoproject.com/en/3.2/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)

# https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", []) + ["localhost", "127.0.0.1"]


DJANGO_APPS = [
    "django.contrib.sites",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    # authentication
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # general
    "rest_framework",
]
LOCAL_APPS = [
    "apps.users",
]

# https://docs.djangoproject.com/en/3.2/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# https://docs.djangoproject.com/en/3.2/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/3.2/ref/settings/#static-root
STATIC_ROOT = BASE_DIR / "apps" / "staticfiles"

# https://docs.djangoproject.com/en/3.2/ref/settings/#media-url
MEDIA_URL = "/media/"
# https://docs.djangoproject.com/en/3.2/ref/settings/#media-root
MEDIA_ROOT = BASE_DIR / "apps" / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"

SITE_ID = 1

# Django REST framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("dj_rest_auth.jwt_auth.JWTCookieAuthentication",)
}

# AUTHENTICATION
REST_USE_JWT = True
REST_AUTH_TOKEN_MODEL = None
JWT_AUTH_REFRESH_COOKIE = "ref_token"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
# вроде про валидацию
# OLD_PASSWORD_FIELD_ENABLED = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"

ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_PRESERVE_USERNAME_CASING = False

# ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "127.0.0.1:8000/here"
# ACCOUNT_SIGNUP_REDIRECT_URL "127.0.0.1:8000/there"

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "1000575426539-46q4dr57cr4hq4v2s648rfqie23ddjs9.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        },
        "SCOPE": [
            "profile",
            "email",
        ],
        "VERIFIED_EMAIL": True,
    }
}

# https://mandrillapp.com/track/click/30166792/miro.com?p=eyJzIjoiSnI4SWRhMkdfNzNTOGNTODY4cDlrMjdmSGZBIiwidiI6MSwicCI6IntcInVcIjozMDE2Njc5MixcInZcIjoxLFwidXJsXCI6XCJodHRwczpcXFwvXFxcL21pcm8uY29tXFxcL2NvbmZpcm0tZW1haWxcXFwvYWdRMlhlWjJzdzNaaVMxNjFtZFFvTkg4UDVwQ1FDS0hcXFwvP3RyYWNrPXRydWUmdXRtX3NvdXJjZT1ub3RpZmljYXRpb24mdXRtX21lZGl1bT1lbWFpbCZ1dG1fY2FtcGFpZ249ZW1haWwtY2hhbmdlLWNvbmZpcm1hdGlvbiZ1dG1fY29udGVudD1jb25maXJtLWVtYWlsLXRyYWNrXCIsXCJpZFwiOlwiZGM2MjRjNDM1YTgyNDU5Njg1ZjllMTNiNWRiOGVkOTdcIixcInVybF9pZHNcIjpbXCI1OTA0NWI0ZTg0MzI5NjAxMzY5MzUzMjJhZGZjZmU5ZDMxNzYyNmJhXCJdfSJ9
