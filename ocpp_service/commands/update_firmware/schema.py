from pandantic import BaseModel


class UpdateFirmwareRequest(BaseModel):
    charger_identify: str

    location: str
    retries: int
    retrieve_date: str
    retry_interval: int


class UpdateFirmwareResponse(BaseModel):
    status: str
