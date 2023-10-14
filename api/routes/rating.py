from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTHeader, JWTBearer
from models import ProductRating, Order, OrderRating, PlaceRating, Product, Place
from models.db_session import get_session
from pydantic_models.order import ProductRatingModel, OrderRatingModel, PlaceRatingModel

router = APIRouter()


@router.post("/product/{product_id}", operation_id="product-rating", summary="Product rating", response_class=Response)
async def send_product_rating(product_id: int, rating: ProductRatingModel, session: AsyncSession = Depends(get_session),
                              token: JWTHeader = Depends(JWTBearer())):
    if await Product.get_product_by_id(product_id, session):
        await ProductRating(product_id=product_id, estimate=rating.estimate, user_id=token.user_id).save(session)
        return Response(status_code=202)
    return Response(status_code=404)


@router.post("/order/{order_id}", operation_id="order-rating", summary="Order rating", response_class=Response)
async def send_order_rating(order_id: int, rating: OrderRatingModel, session: AsyncSession = Depends(get_session),
                            token: JWTHeader = Depends(JWTBearer())):
    order = await Order.get_order_by_id(order_id, session)
    if order and order.user_id == token.user_id:
        await OrderRating(order_id=order_id, order_estimate=rating.order_estimate,
                          delivery_estimate=rating.delivery_estimate).save(session)
        return Response(status_code=202)
    return Response(status_code=404)


@router.post("/place/{place_id}", operation_id="place-rating", summary="Place rating", response_class=Response)
async def send_place_rating(place_id: int, rating: PlaceRatingModel, session: AsyncSession = Depends(get_session),
                            token: JWTHeader = Depends(JWTBearer())):
    if await Place.get_by_place_id(place_id, session):
        await PlaceRating(user_id=token.user_id, estimate=rating.estimate, place_id=place_id).save(session)
        return Response(status_code=202)
    return Response(status_code=404)


@router.get("/product/{product_id}", operation_id="get-product-rating", summary="User estimate of product if exists",
            response_model=ProductRatingModel)
async def get_product_rating(product_id: int, session: AsyncSession = Depends(get_session),
                             token: JWTHeader = Depends(JWTBearer())):
    if product_rating := await ProductRating.get_by_product_id(product_id, token.user_id, session):
        return ProductRatingModel.model_validate(product_rating)
    return Response(status_code=404)


@router.get("/order/{order_id}", operation_id="get-order-rating", summary="User estimate of order if exists",
            response_model=OrderRatingModel)
async def get_order_rating(order_id: int, session: AsyncSession = Depends(get_session),
                           token: JWTHeader = Depends(JWTBearer())):
    if order_rating := await OrderRating.get_by_order_id(order_id, token.user_id, session):
        return OrderRatingModel.model_validate(order_rating)
    return Response(status_code=404)


@router.get("/place/{place_id}", operation_id="get-place-rating", summary="User estimate of place if exists",
            response_model=PlaceRatingModel)
async def get_place_rating(place_id: int, session: AsyncSession = Depends(get_session),
                           token: JWTHeader = Depends(JWTBearer())):
    if place_rating := await PlaceRating.get_by_place_id(place_id, token.user_id, session):
        return PlaceRatingModel.model_validate(place_rating)
    return Response(status_code=404)
