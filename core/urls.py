from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .schema import swagger_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/common/", include("apps.common.urls", namespace="common")),
    path("api/v1/users/", include("apps.users.urls", namespace="users")),
    path("api/v1/chargers/", include("apps.chargers.urls", namespace="chargers")),
    path("api/v1/ocpp_messages/", include("apps.ocpp_messages.urls", namespace="ocpp_messages"))
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
