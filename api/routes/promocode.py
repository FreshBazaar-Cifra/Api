from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTHeader, JWTBearer
from models import Order, Position, Promocode, Product
from models.db_session import get_session
from pydantic_models.order import PromocodeCheckIn, PromocodeCheckOut

router = APIRouter()


@router.get("/price", dependencies=[Depends(JWTBearer())], operation_id="promo-price",
            summary="Get new price by code", response_model=PromocodeCheckIn)
async def get_new_price(code: str, price: float, session: AsyncSession = Depends(get_session)):
    if promocode := await Promocode.get(code, session):
        return {"price": price * (1 - price * promocode.sale // 100)}
    return Response(status_code=404)
