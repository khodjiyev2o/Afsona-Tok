from pandantic import BaseModel


class RemoteStopRequest(BaseModel):
    transaction_id: int


class RemoteStopResponse(BaseModel):
    status: bool
