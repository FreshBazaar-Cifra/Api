from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTHeader, JWTBearer
from descriptions.order import *
from models import Order, Position, Promocode, Product
from models.db_session import get_session
from pydantic_models.order import OrderModel, PaymentLink, CreateOrderModel

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


@router.post("/create", summary="Create order", operation_id="create-order",
             description=create_order_description, response_model=PaymentLink)
async def create_order_(create_order: CreateOrderModel, session: AsyncSession = Depends(get_session),
                        token: JWTHeader = Depends(JWTBearer())):
    promocode = await Promocode.get_by_id(create_order.promocode_id, session=session)
    if not promocode:
        promocode = 0
    products = await Product.get_by_ids(list(map(lambda position: position.product_id, create_order.positions)), session)
    price = sum(map(lambda product: product.price, products))
    if promocode:
        price = price * (1 - promocode.sale // 100)
    delivery_price = 100
    total = price + delivery_price

    order = Order(user_id=token.user_id, address_id=create_order.address_id, delivery_price=delivery_price, price=price,
                  total=total, market_id=create_order.market_id)
    await order.save(session)
    await session.refresh(order)
    for position in create_order.positions:
        _ = Position(product_id=position.product_id, count=position.count)
        await _.save(session)
        order.positions.append(_)
    await session.commit()
    return PaymentLink(url="asdasdadsd", amount=111)
