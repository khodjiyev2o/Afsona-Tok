from pandantic import BaseModel


class ChangeConfigurationRequest(BaseModel):
    charger_identify: str
    key: str
    value: str


class ChangeConfigurationResponse(BaseModel):
    status: bool
