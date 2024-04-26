from pandantic import BaseModel


class CancelReservationRequest(BaseModel):
    charger_identify: str
    reservation_id: int


class CancelReservationResponse(BaseModel):
    status: bool
