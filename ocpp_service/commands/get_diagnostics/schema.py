from typing import Optional

from pandantic import BaseModel


class GetDiagnosticsRequest(BaseModel):
    charger_identify: str

    location: str
    retries: Optional[int] = None
    retry_interval: Optional[int] = None
    start_time: Optional[str] = None
    stop_time: Optional[str] = None


class GetDiagnosticsResponse(BaseModel):
    status: str
    file_name: Optional[str] = None
