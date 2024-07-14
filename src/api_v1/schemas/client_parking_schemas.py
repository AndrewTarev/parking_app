from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BaseClientParking(BaseModel):
    client_id: int
    parking_id: int


class ClientParkingIn(BaseClientParking):
    pass


class ClientParkingOut(BaseClientParking):
    model_config = ConfigDict(from_attributes=True)
    id: int
    time_in: datetime
    time_out: datetime | None


class ClientParkingDelete(BaseClientParking):
    time_out: datetime | None
