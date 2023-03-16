from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AccessLevelViewSet, ParticipantViewSet, ProfessionViewSet

router = DefaultRouter()
router.register("access_levels", AccessLevelViewSet, basename="access_level")
router.register("participants", ParticipantViewSet, basename="participant")
router.register("professions", ProfessionViewSet, basename="profession")

v1_urls = [
    path("v1/", include(router.urls)),
]

urlpatterns = [
    path("", include(v1_urls)),
]
