from django.contrib import admin
from django.urls import include, path

from apps.authentication.urls import dummy_front_urls as auth_dummy_urls
from apps.authentication.urls import urlpatterns as v1_auth_urls

api_urls = [
    path("api/", include(v1_auth_urls)),
]

urlpatterns = [
    path("admin/", admin.site.urls),
]

urlpatterns += api_urls
urlpatterns += auth_dummy_urls


from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns += [
    # YOUR PATTERNS
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
