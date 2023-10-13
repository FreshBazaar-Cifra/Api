from pydantic import BaseModel, ConfigDict


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    phone: str | None = None
    email: str | None = None
    login: str


class LoginIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    login: str
    password: str


class LoginOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str
    user: UserModel


class RegisterIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str | None = None
    login: str
    password: str


class RegisterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    token: str
    user: UserModel


class ChangeUserIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
