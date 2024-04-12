from django.urls import path
from .api_endpoints import *


app_name = 'chargers'


urlpatterns = [
    path("StartChargingCommand/", StartChargingCommandView.as_view(), name="start-charging-command"),
    path("MapLocationList/", MapLocationListView.as_view(), name="map-location-list"),
    path("StopChargingCommand/", StopChargingCommandView.as_view(), name="stop-charging-command"),
]
