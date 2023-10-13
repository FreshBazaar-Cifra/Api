from datetime import time

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.types import Decimal


class MarketModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    images: list[str]
    city: str
    street: str | None = None
    district: str | None = None
    house: str
    latitude: Decimal
    longitude: Decimal


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


class PlaceModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    logo: str
    description: str
    location_photo: str
    phones: list[str]
    working_hours: list[WorkingHourModel]
