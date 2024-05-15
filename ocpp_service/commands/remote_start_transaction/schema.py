from pandantic import BaseModel


class RemoteStartRequest(BaseModel):
    charger_identify: str

    id_tag: str
    connector_id: int


class RemoteStartResponse(BaseModel):
    status: bool
