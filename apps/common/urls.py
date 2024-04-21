from django.urls import path

from .api_endpoints import * # noqa

app_name = 'common'

urlpatterns = [
    path("AppealTypeList/", AppealTypeListView.as_view(), name="appeal-type-list"),
    path("UserAppealCreate/", UserAppealCreateView.as_view(), name="user-appeal-create"),
    path("FrontendTranslations/", FrontendTranslationView.as_view(), name="frontend-translations"),
    path("ConnectTypeList/", ConnectionTypeListView.as_view(), name="connection-type-list"),
    path("ManufacturerList/", ManufacturerListView.as_view(), name="manufacturer-list"),
    path("CarModelList/", CarModelListView.as_view(), name="car-model-list"),
    path("UserCarAdd/", UserCarAddView.as_view(), name="user-car-add"),
    path("UserCarEdit/<int:pk>/", UserCarEditView.as_view(), name="user-car-edit"),
    path("UserCarList/", UserCarListView.as_view(), name="user-car-list"),
    path("UserCarDelete/<int:pk>/", UserCarDeleteView.as_view(), name="user-car-delete"),
    path("MainSettings/", MainSettingsView.as_view(), name="main-settings"),
    path("SavedLocation/", SavedLocationAPIView.as_view(), name="saved-location"),
]
