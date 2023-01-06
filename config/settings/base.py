from datetime import timedelta
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
    # authentication apps
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    # general apps
    "rest_framework",
]
LOCAL_APPS = [
    "apps.users",
    "apps.authentication",
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


# -------------------------------- AUTHENTICATION -------------------------------------

# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"

SITE_ID = 1

AUTHENTICATION_BACKENDS = ("allauth.account.auth_backends.AuthenticationBackend",)

# Django REST framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("dj_rest_auth.jwt_auth.JWTCookieAuthentication",)
}

# dj-rest-auth
# https://dj-rest-auth.readthedocs.io/en/latest/configuration.html
REST_USE_JWT = True
REST_AUTH_TOKEN_MODEL = None
JWT_AUTH_REFRESH_COOKIE = "ref_token"
JWT_AUTH_SECURE = True
REST_AUTH_SERIALIZERS = {
    "JWT_SERIALIZER": "apps.authentication.serializers.LoginJWTSerializer",
}

# Simple JWT
SIMPLE_JWT = {
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#access-token-lifetime
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html#rotate-refresh-tokens
    "ROTATE_REFRESH_TOKENS": True,
}

# https://docs.djangoproject.com/en/3.2/ref/settings/#login-url
LOGIN_URL = "/auth/"

# django-allauth
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
SOCIALACCOUNT_ADAPTER = "apps.authentication.adapters.SocialAccountAdapter"
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": "1000575426539-46q4dr57cr4hq4v2s648rfqie23ddjs9.apps.googleusercontent.com",
            "secret": "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",
            "key": "",
        },
        "VERIFIED_EMAIL": True,
    }
}

# URLs for sending confirmation emails to the frontend.
FRONTEND_EMAIL_CONFIRM_URL = "auth/email/confirm/"
FRONTEND_PASS_RESET_CONFIRM_URL = "auth/password/reset/confirm/"


# -------------------------------- SENDING EMAIL -------------------------------------

# https://docs.djangoproject.com/en/3.2/ref/settings/#std-setting-EMAIL_BACKEND
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
