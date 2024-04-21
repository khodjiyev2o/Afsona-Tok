from django.urls import path
from .api_endpoints import *


app_name = 'chargers'


urlpatterns = [
    path("StartChargingCommand/", StartChargingCommandView.as_view(), name="start-charging-command"),
    path("MapLocationList/", MapLocationListView.as_view(), name="map-location-list"),
    path("LocationList/", LocationListView.as_view(), name="location-list"),
    path("StopChargingCommand/", StopChargingCommandView.as_view(), name="stop-charging-command"),
    path("LocationDetail/<int:pk>/", LocationDetailView.as_view(), name="location-detail"),
    path("ConnectorDetail/<int:pk>/", ConnectorDetailView.as_view(), name="connector-detail"),
    path("ChargingTransactionList/", ChargingTransactionListAPIView.as_view(), name='charging-transaction-list'),
    path("ChargingTransactionDetail/<int:pk>/", ChargingTransactionDetailAPIView.as_view(), name='charging-transaction-detail'),
    path('SavedLocationList/', SavedLocationListView.as_view(), name='saved-location-list')
]
