from typing import Annotated, Self

from annotated_types import Ge, Le
from pydantic import BaseModel, ConfigDict, model_validator


class BaseParking(BaseModel):
    address: str
    opened: bool
    count_places: Annotated[int, Ge(0), Le(100)]
    count_available_places: Annotated[int, Ge(0), Le(100)]


class ParkingIn(BaseParking):
    @model_validator(mode="after")
    def check_count_available_places(self) -> Self:
        cnt_plc = self.count_places
        cnt_available = self.count_available_places
        if cnt_available > cnt_plc:
            raise ValueError(
                "Свободных мест не может быть больше общего количества мест"
            )
        return self


class ParkingOut(BaseParking):
    model_config = ConfigDict(from_attributes=True)
    id: int
