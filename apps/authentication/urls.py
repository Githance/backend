from django.urls import path

from .views import GoogleLoginCallbackView, GoogleLoginView

urlpatterns = [
    path("auth/google/login/", GoogleLoginView.as_view(), name="google_login"),
    path(
        "auth/google/login/callback/",
        GoogleLoginCallbackView.as_view(),
        name="google_callback",
    ),
]
