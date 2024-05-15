from ocpp.v16.enums import ResetType
from pandantic import BaseModel


class ResetRequest(BaseModel):
    charger_identify: str

    reset_type: ResetType


class ResetResponse(BaseModel):
    status: str
