from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer
from descriptions.market import get_all_markets_description, get_market_by_id_description
from models import Market
from models.db_session import get_session
from pydantic_models.place import MarketModel

router = APIRouter()


@router.get("/all", summary="Markets", operation_id="markets", dependencies=[Depends(JWTBearer())],
            description=get_all_markets_description, response_model=list[MarketModel])
async def get_all_markets(page: int, limit: int, session: AsyncSession = Depends(get_session)):
    markets = await Market.get_all(page, limit, session)
    return [
        MarketModel.model_validate(market)
        for market in markets
    ]


@router.get("/id/{market_id}", summary="Get market by id", operation_id="market-by-id", dependencies=[Depends(JWTBearer())],
            description=get_market_by_id_description, response_model=MarketModel)
async def get_market_by_id(market_id: int, session: AsyncSession = Depends(get_session)):
    if market := await Market.get_by_market_id(market_id, session):
        return MarketModel.model_validate(market)
    return Response(status_code=404)

