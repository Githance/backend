from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.authentication.urls import dummy_front_urls as auth_dummy_urls

apps_urls = [
    path("", include("apps.authentication.urls")),
    path("", include("apps.users.urls")),
    path("", include("apps.projects.urls")),
    path("", include("apps.participants.urls")),
]

openapi_urls = [
    path("", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns = []

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns += [
        path("admin/__debug__/", include(debug_toolbar.urls)),
    ]

urlpatterns += [
    path("admin/", admin.site.urls),
    path("api/", include(apps_urls)),
    path("api/schema/", include(openapi_urls)),
    path("", include(auth_dummy_urls)),
]
