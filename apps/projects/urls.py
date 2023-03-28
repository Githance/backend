from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")

v1_urls = [
    path("v1/", include(router.urls)),
]

urlpatterns = [
    path("", include(v1_urls)),
]
