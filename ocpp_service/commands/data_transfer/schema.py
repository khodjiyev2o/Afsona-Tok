from typing import Optional, Any

from pandantic import BaseModel


class DataTransferRequest(BaseModel):
    charger_identify: str

    vendor_id: str
    message_id: Optional[str] = None
    data: Optional[Any] = None


class DataTransferResponse(BaseModel):
    status: str
    data: Optional[Any] = None
