from typing import Optional

from pandantic import BaseModel


class GetLocalListVersionRequest(BaseModel):
    charger_identify: str


class GetLocalListVersionResponse(BaseModel):
    status: str
    list_version: Optional[int] = None
