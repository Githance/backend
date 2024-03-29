from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, VacancyViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet, basename="project")
router.register("vacancies", VacancyViewSet, basename="vacancy")

v1_urls = [
    path("v1/", include(router.urls)),
]

urlpatterns = [
    path("", include(v1_urls)),
]
