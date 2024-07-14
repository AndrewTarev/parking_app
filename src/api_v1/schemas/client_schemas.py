from pydantic import BaseModel, ConfigDict, field_validator


class BaseClient(BaseModel):
    name: str
    surname: str
    credit_card: str
    car_number: str


class ClientIn(BaseClient):

    @field_validator("name", "surname")
    @classmethod
    def validate(cls, v: str):
        return v.strip().title()


class ClientOut(BaseClient):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ClientUpdate(BaseClient):
    pass


class ClientUpdatePartial(BaseClient):
    name: str | None = None
    surname: str | None = None
    credit_card: str | None = None
    car_number: str | None = None
