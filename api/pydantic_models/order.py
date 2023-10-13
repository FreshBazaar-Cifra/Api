from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic.types import Decimal


class DeliverymanModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    reg_date: str
    phone: str

    @field_validator('reg_date', mode='before')
    @classmethod
    def format_date_of_taking(cls, value):
        if value and isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='seconds')


class PromocodeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sale: int
    code: int


class PromocodeCheckIn(BaseModel):
    code: str
    price: float


class PromocodeCheckOut(BaseModel):
    price: float


class OrderModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: str
    status: str
    deliveryman: DeliverymanModel
    price: float
    delivery_price: float
    promocode: PromocodeModel | None = None
    total: float

    @field_validator('date', mode='before')
    @classmethod
    def format_date_of_taking(cls, value) -> str:
        if value and isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='seconds')


class PaymentLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str
    amount: float


class PositionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    product_id: int
    count: int


class AttributeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: str
    product_id: int


class ProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    place_id: int
    description: str
    images: list[str]
    name: str
    price: Decimal
    attributes: list[AttributeModel]
