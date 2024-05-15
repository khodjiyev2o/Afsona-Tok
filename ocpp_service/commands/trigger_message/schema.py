from typing import Optional

from ocpp.v16.enums import MessageTrigger
from pandantic import BaseModel


class TriggerMessageRequest(BaseModel):
    charger_identify: str

    trigger_message: MessageTrigger
    connector_id: Optional[int] = None


class TriggerMessageResponse(BaseModel):
    status: str
