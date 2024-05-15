from ocpp.v16.enums import AvailabilityType
from pandantic import BaseModel


class ChangeAvailabilityRequest(BaseModel):
    charger_identify: str

    connector_id: int
    availability_type: AvailabilityType


class ChangeAvailabilityResponse(BaseModel):
    status: str
