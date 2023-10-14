from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTHeader, JWTBearer
from models import Product, Favorite
from models.db_session import get_session
from pydantic_models.order import ProductModel

router = APIRouter()


@router.put("/{product_id}", operation_id="add-favorite",
            summary="Add to favorite", response_class=Response)
async def add_to_favorite(product_id: int, session: AsyncSession = Depends(get_session),
                          token: JWTHeader = Depends(JWTBearer())):
    favorite = await Favorite.get_by_user(token.user_id, session)
    if not favorite:
        favorite = Favorite(user_id=token.user_id)
        await favorite.save(session)

    product = await Product.get_product_by_id(product_id, session)
    if product:
        favorite.products.append(product)
        await session.commit()
        return Response(status_code=202)
    return Response(status_code=404)


@router.get("/", operation_id="get-favorite", summary="Get favorites", response_model=list[ProductModel])
async def get_favorites(session: AsyncSession = Depends(get_session), token: JWTHeader = Depends(JWTBearer())):
    if favorite := await Favorite.get_by_user(token.user_id, session):
        return [ProductModel.model_validate(product) for product in favorite.products]
    return []

