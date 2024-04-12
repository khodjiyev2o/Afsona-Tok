from pandantic import BaseModel


class RemoteStopRequest(BaseModel):
    transaction_id: int
    charger_identify: str
    id_tag: str


class RemoteStopResponse(BaseModel):
    status: bool
