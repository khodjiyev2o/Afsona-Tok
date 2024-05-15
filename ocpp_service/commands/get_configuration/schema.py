from typing import Optional, List

from pandantic import BaseModel


class GetConfigurationRequest(BaseModel):
    charger_identify: str

    keys: List[str]


class GetConfigurationResponse(BaseModel):
    status: str

    configuration_key: Optional[List] = None
    unknown_key: Optional[List] = None

