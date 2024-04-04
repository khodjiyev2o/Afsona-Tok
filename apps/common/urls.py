from django.urls import path

from .api_endpoints import FrontendTranslationView

app_name = 'common'

urlpatterns = [
    path("FrontendTranslations/", FrontendTranslationView.as_view(), name="frontend-translations"),
]
