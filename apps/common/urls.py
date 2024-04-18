from django.urls import path

from .api_endpoints import * # noqa


app_name = 'common'

urlpatterns = [
    path("FrontendTranslations/", FrontendTranslationView.as_view(), name="frontend-translations"),
    path("ConnectTypeList/", ConnectionTypeListView.as_view(), name="connection-type-list"),
    path("ManufacturerList/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("CarModelList/", CarModelListView.as_view(), name="car-model-list"),
    path("UserCarAdd/", UserCarAddView.as_view(), name="user-car-add"),
    path("UserCarList/", UserCarListView.as_view(), name="user-car-list"),
    path("MainSettings/", MainSettingsView.as_view(), name="main-settings"),
    path("SavedLocations/", SavedLocationAPIView.as_view(), name="saved-locations"),
    path("InstructionList/", InstructionListAPIView.as_view(), name="instruction-list"),
]
