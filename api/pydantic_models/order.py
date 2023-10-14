from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator, model_validator
from pydantic.types import PositiveInt

from models import ProductRating
from pydantic_models.place import AddressModel, MarketModel


class DeliverymanModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
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

    id: PositiveInt
    sale: int
    code: str


class PromocodeCheckIn(BaseModel):
    code: str
    price: float


class PromocodeCheckOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    price: float


class PaymentLink(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    url: str
    amount: float


class AttributeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    value: str


class ProductCategoryModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    name: str


class ProductModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    place_id: int
    description: str
    images: list[str]
    name: str
    price: float
    weight: int
    category: ProductCategoryModel
    estimate: float | None = None
    attributes: list[AttributeModel]


class PositionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product: ProductModel
    count: int


class OrderPositionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    count: int


class OrderModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    date: str
    status: Literal["ordered", "paid", "confirmed", "delivered"]
    deliveryman: DeliverymanModel | None = None
    market: MarketModel
    address: AddressModel
    positions: list[PositionModel]
    price: float
    delivery_price: float
    promocode: PromocodeModel | None = None
    total: float

    @field_validator('date', mode='before')
    @classmethod
    def format_date_of_taking(cls, value) -> str:
        if value and isinstance(value, datetime):
            return value.isoformat(sep=' ', timespec='seconds')


class CreateOrderModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    address_id: PositiveInt
    market_id: int
    positions: list[OrderPositionModel]
    promocode_id: int | None = None


class OrderRatingModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    order_estimate: PositiveInt
    delivery_estimate: PositiveInt


class ProductRatingModel(BaseModel):
    estimate: float
