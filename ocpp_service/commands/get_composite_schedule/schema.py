from typing import Optional, Dict
from ocpp.v16.enums import ChargingRateUnitType

from pandantic import BaseModel


class GetCompositeScheduleRequest(BaseModel):
    charger_identify: str

    connector_id: int
    duration: int
    charging_rate_unit: ChargingRateUnitType


class GetCompositeScheduleResponse(BaseModel):
    status: str
    connector_id: Optional[int] = None
    schedule_start: Optional[str] = None
    charging_schedule: Optional[Dict] = None
