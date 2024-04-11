from django.urls import path

from .api_endpoints import FrontendTranslationView, ManufacturerListView

app_name = 'common'

urlpatterns = [
    path("FrontendTranslations/", FrontendTranslationView.as_view(), name="frontend-translations"),
    path("ManufacturerList/", ManufacturerListView.as_view(), name="manufacturer-list"),
]
