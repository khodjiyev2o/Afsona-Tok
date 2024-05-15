from pandantic import BaseModel


class UnlockConnectorRequest(BaseModel):
    charger_identify: str

    connector_id: int


class UnlockConnectorResponse(BaseModel):
    status: str
