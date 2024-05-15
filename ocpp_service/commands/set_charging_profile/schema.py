from ocpp.v16.datatypes import ChargingProfile
from pandantic import BaseModel


class SetChargingProfileRequest(BaseModel):
    charger_identify: str

    connector_id: int
    cs_charging_profiles: ChargingProfile


class SetChargingProfileResponse(BaseModel):
    status: str
