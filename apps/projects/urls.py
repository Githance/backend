from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjectStatusViewSet, ProjectTypeViewSet, ProjectViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("project_statuses", ProjectStatusViewSet)
router.register("project_types", ProjectTypeViewSet)

v1_urls = [
    path("v1/", include(router.urls)),
]

urlpatterns = [
    path("", include(v1_urls)),
]
