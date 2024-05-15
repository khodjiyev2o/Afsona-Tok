from typing import Optional

from pandantic import BaseModel


class ReserveNowRequest(BaseModel):
    charger_identify: str

    connector_id: int
    expiry_date: str
    parent_id_tag: Optional[str] = None
    reservation_id: int


class ReserveNowResponse(BaseModel):
    status: str
