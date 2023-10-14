from fastapi import APIRouter, Depends, Response
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTHeader, JWTBearer
from models import Product, Favorite, Basket, Position
from models.db_session import get_session
from pydantic_models.order import PositionModel

router = APIRouter()


@router.put("/add/{product_id}", operation_id="add-basket",
            summary="Add to Basket", response_class=Response)
async def add_to_basket(product_id: PositiveInt, count: PositiveInt, session: AsyncSession = Depends(get_session),
                        token: JWTHeader = Depends(JWTBearer())):
    basket = await Basket.get_by_user(token.user_id, session)
    if not basket:
        basket = Basket(user_id=token.user_id)
        await basket.save(session)

    product = await Product.get_product_by_id(product_id, session)
    if product:
        position = Position(product_id=product_id, count=count)
        await position.save(session)
        basket.positions.append(position)
        await session.commit()
        return Response(status_code=202)
    return Response(status_code=404)


@router.get("/", operation_id="get-basket", summary="Get basket", response_model=list[PositionModel])
async def get_favorites(session: AsyncSession = Depends(get_session), token: JWTHeader = Depends(JWTBearer())):
    if basket := await Basket.get_by_user(token.user_id, session):
        return [PositionModel.model_validate(position) for position in basket.positions]
    return []


@router.put("/change-count/{position_id}", operation_id="change-count", summary="Change basket item count",
            response_class=Response)
async def change_position_count(position_id: PositiveInt, count: PositiveInt,
                                session: AsyncSession = Depends(get_session),
                                token: JWTHeader = Depends(JWTBearer())):
    basket = await Basket.get_by_user(token.user_id, session)
    for position in basket.positions:
        if position.id == position_id:
            position.count = count
            await session.commit()
            return Response(status_code=202)
    return Response(status_code=404)


@router.delete("/position/{position_id}", operation_id="delete-position", summary="Delete position from basket",
               response_class=Response)
async def delete_position_count(position_id: PositiveInt, session: AsyncSession = Depends(get_session),
                                token: JWTHeader = Depends(JWTBearer())):
    basket = await Basket.get_by_user(token.user_id, session)
    for position in basket.positions:
        if position.id == position_id:
            basket.positions.remove(position)
            await session.delete(position)
            await session.commit()
            return Response(status_code=202)
    return Response(status_code=404)
