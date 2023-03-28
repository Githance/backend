from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccessLevelViewSet, ProfessionViewSet

router = DefaultRouter()
router.register("access_levels", AccessLevelViewSet, basename="access-level")
router.register("professions", ProfessionViewSet, basename="profession")

v1_urls = [
    path("v1/", include(router.urls)),
]

urlpatterns = [
    path("", include(v1_urls)),
]
