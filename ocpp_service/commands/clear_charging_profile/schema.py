from typing import Optional

from pandantic import BaseModel


class ClearChargingProfileRequest(BaseModel):
    charger_identify: str

    charger_profile_id: Optional[int] = None
    connector_id: Optional[int] = None
    charging_profile_purpose: Optional[str] = None
    stack_level: Optional[int] = None


class ClearChargingProfileResponse(BaseModel):
    status: str
