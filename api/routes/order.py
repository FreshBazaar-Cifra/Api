from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTHeader, JWTBearer
from descriptions.order import *
from models import Order
from models.db_session import get_session
from pydantic_models.order import OrderModel, PaymentLink

router = APIRouter()


@router.get("/all", summary="Order", operation_id="orders",
            description=get_all_orders_description, response_model=list[OrderModel])
async def get_orders(session: AsyncSession = Depends(get_session),
                       token: JWTHeader = Depends(JWTBearer())):
    orders = await Order.get_orders_by_user(token.user_id, session)
    return [
        OrderModel.model_validate(order)
        for order in orders
    ]


@router.get("/id/{order_id}", summary="Get order by id", operation_id="order-by-id",
            description=get_order_by_id_description, response_model=OrderModel)
async def get_product_by_id(order_id: int, session: AsyncSession = Depends(get_session),
                            token: JWTHeader = Depends(JWTBearer())):
    if order := await Order.get_order_by_id(order_id, token.user_id, session):
        return OrderModel.model_validate(order)
    return Response(status_code=404)


# @router.post("/create", summary="Create order", operation_id="create-order",
#              description=create_order_description, response_model=PaymentLink)