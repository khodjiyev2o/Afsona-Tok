from pandantic import BaseModel


class ClearClearCacheRequest(BaseModel):
    charger_identify: str


class ClearClearCacheResponse(BaseModel):
    status: str

