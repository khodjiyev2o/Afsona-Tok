from pandantic import BaseModel


class RemoteStopRequest(BaseModel):
    charger_identify: str

    transaction_id: int
    id_tag: str


class RemoteStopResponse(BaseModel):
    status: bool
