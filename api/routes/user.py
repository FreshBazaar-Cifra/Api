from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer, JWTHeader
from descriptions.user import *
from models import User
from models.db_session import get_session
from pydantic_models.user import UserModel

router = APIRouter()


@router.get("/", summary="Get user", operation_id="user",
            description=get_user_description, response_model=UserModel)
async def get_user(token: JWTHeader = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)):
    if user := await User.get_by_id(token.user_id, session=session):
        return UserModel.model_validate(user)
    return Response(status_code=404)
