from django.urls import path


from config.definitions import DEBUG
from .api.views import HomeView


if DEBUG:
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Bumblebee API",
            default_version="v1",
            description="API Docs for Bumblebee social media",
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    docs_urls = [
        path(
            "swagger-docs/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger",
        ),
        path(
            "redoc-docs/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
] + docs_urls
