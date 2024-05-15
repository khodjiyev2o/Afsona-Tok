from typing import Optional

from ocpp.v16.datatypes import AuthorizationData
from ocpp.v16.enums import UpdateType
from pandantic import BaseModel


class SendLocalListRequest(BaseModel):
    charger_identify: str

    list_version: int
    local_authorization_list: list[AuthorizationData]
    update_type: UpdateType


class SendLocalListResponse(BaseModel):
    status: str

