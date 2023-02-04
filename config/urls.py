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
]

openapi_urls = [
    path("", SpectacularAPIView.as_view(api_version="v2"), name="schema"),
    path(
        "swagger-ui/",
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
urlpatterns += [
    path("admin/", admin.site.urls),
    path("api/", include(apps_urls)),
    path("api/schema/", include(openapi_urls)),
    path("", include(auth_dummy_urls)),
]
