from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer
from descriptions.place import get_all_places_by_market_description, get_place_by_id_description
from models import Place, PlaceRating
from models.db_session import get_session
from pydantic_models.place import PlaceModel

router = APIRouter()


@router.get("/all", summary="Places", operation_id="places", dependencies=[Depends(JWTBearer())],
            description=get_all_places_by_market_description, response_model=list[PlaceModel])
async def get_places_by_market(market_id: int, page: int, limit: int, session: AsyncSession = Depends(get_session)):
    places = await Place.get_all_by_market(market_id, page, limit, session)
    places_ = []
    for place in places:
        place.estimate = await PlaceRating.get_average_estimate(place.id, session)
        places_.append(PlaceModel.model_validate(place))
    return places_


@router.get("/id/{place_id}", summary="Get place by id", operation_id="place-by-id", dependencies=[Depends(JWTBearer())],
            description=get_place_by_id_description, response_model=PlaceModel)
async def get_place_by_id(place_id: int, session: AsyncSession = Depends(get_session)):
    if place := await Place.get_by_place_id(place_id, session):
        place.estimate = await PlaceRating.get_average_estimate(place.id, session)
        return PlaceModel.model_validate(place)
    return Response(status_code=404)
