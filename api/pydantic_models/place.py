from datetime import time

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.types import Decimal, PositiveInt
from pydantic_extra_types.coordinate import Latitude, Longitude


class WorkingHourModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day_of_week: int
    opening_time: str
    closing_time: str

    @field_validator('opening_time', 'closing_time', mode='before')
    @classmethod
    def format_date_of_taking(cls, value) -> str:
        if value and isinstance(value, time):
            return value.strftime('%H:%M')


class AddressModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str
    district: str | None = None
    street: str
    home: str
    entrance: str | None = None
    apartment: str | None = None
    intercom: str | None = None
    latitude: Latitude
    longitude: Longitude


class MarketModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    name: str
    images: list[str]
    address: AddressModel
    working_hours: list[WorkingHourModel]


class PlaceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    name: str
    logo: str
    description: str
    location_photo: str
    phones: list[str]
    market: MarketModel
    working_hours: list[WorkingHourModel]

