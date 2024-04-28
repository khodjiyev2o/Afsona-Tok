from enum import Enum

from pandantic import BaseModel


class ResetTypeEnum(Enum):
    soft = 'Soft'
    hard = 'Hard'


class ResetRequest(BaseModel):
    charger_identify: str
    reset_type: ResetTypeEnum


class ResetResponse(BaseModel):
    status: bool
