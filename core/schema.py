from django.urls import re_path, path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .generator import BothHttpAndHttpsSchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="AFSONA TOK API",
        default_version="v1",
        description="AFSONA TOK",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="samandarkhodjiyev@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    generator_class=BothHttpAndHttpsSchemaGenerator,
    permission_classes=[permissions.AllowAny,],
    patterns=[
        path("api/v1/common/", include("apps.common.urls", namespace="common")),
        path("api/v1/users/", include("apps.users.urls", namespace="users")),
        path('api/v1/chargers/', include('apps.chargers.urls', namespace='chargers')),
        path("api/v1/ocpp_messages/", include("apps.chargers.ocpp_messages.urls", namespace="ocpp_messages")),
        path("api/v1/payment/", include("apps.payment.urls", namespace="payment"))
    ]
)
swagger_urlpatterns = [
    re_path(
        r"^docs(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^docs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
