from pandantic import BaseModel


class ChangeConfigurationRequest(BaseModel):
    charger_identify: str


class ChangeConfigurationResponse(BaseModel):
    status: bool
