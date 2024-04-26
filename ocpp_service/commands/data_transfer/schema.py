from pandantic import BaseModel


class RemoteStartRequest(BaseModel):
    id_tag: str
    charger_identify: str
    connector_id: int


class RemoteStartResponse(BaseModel):
    status: bool
