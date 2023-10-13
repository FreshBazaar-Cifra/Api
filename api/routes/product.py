from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer
from descriptions.product import get_all_products_description, get_product_by_id_description
from models import Product
from models.db_session import get_session
from pydantic_models.order import ProductModel

router = APIRouter()


@router.get("/all", summary="Products", operation_id="products", dependencies=[Depends(JWTBearer())],
            description=get_all_products_description, response_model=list[ProductModel])
async def get_products(place_id: int, page: int, limit: int, session: AsyncSession = Depends(get_session)):
    products = await Product.get_all_by_place_id(place_id, page, limit, session)
    return [
        ProductModel.model_validate(product)
        for product in products
    ]


@router.get("/id/{product_id}", summary="Get product by id", operation_id="product-by-id", dependencies=[Depends(JWTBearer())],
            description=get_product_by_id_description, response_model=ProductModel)
async def get_product_by_id(product_id: int, session: AsyncSession = Depends(get_session)):
    if product := await Product.get_product_by_id(product_id, session):
        return ProductModel.model_validate(product)
    return Response(status_code=404)
