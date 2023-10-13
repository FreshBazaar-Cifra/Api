from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from auth.auth_bearer import JWTBearer, JWTHeader
from auth.auth_handler import sign_jwt
from descriptions.user import *
from models import User
from models.db_session import get_session
from pydantic_models.user import LoginOut, LoginIn, RegisterIn, RegisterOut, UserModel, ChangeUserIn
from utils.password import hash_password

router = APIRouter()


@router.post("/login", summary="Login", operation_id="login",
             description=login_user_description, response_model=LoginOut)
async def login_user(login: LoginIn, session: AsyncSession = Depends(get_session)):
    user = await User.get_by_login(login.login, session)
    if user and user.password == hash_password(login.password):
        return {"token": sign_jwt(user.id), "user": UserModel.model_validate(user)}
    return Response(status_code=403)


@router.get("/", summary="Get user", operation_id="user",
            description=get_user_description, response_model=UserModel)
async def get_user(token: JWTHeader = Depends(JWTBearer()), session: AsyncSession = Depends(get_session)):
    if user := await User.get_by_id(token.user_id, session=session):
        return UserModel.model_validate(user)
    return Response(status_code=404)


@router.post("/register", summary="Register", operation_id="register",
             description=register_user_description, response_model=RegisterOut)
async def register_user(register: RegisterIn, session: AsyncSession = Depends(get_session)):
    user = User(first_name=register.first_name, last_name=register.last_name, login=register.login,
                password=hash_password(register.password))
    await user.save(session)
    return {"token": sign_jwt(user.id), "user": UserModel.model_validate(user)}


@router.post("/change-info", summary="Change user info", operation_id="change-user-info",
             description=change_user_info_description, response_class=Response, status_code=202)
async def change_user_info(change: ChangeUserIn, token: JWTHeader = Depends(JWTBearer()),
                           session: AsyncSession = Depends(get_session)):
    await User.change_user_names(token.user_id, change.first_name, change.last_name, session)
