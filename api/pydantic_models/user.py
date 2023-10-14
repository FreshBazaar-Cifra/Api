from pydantic import BaseModel, ConfigDict, PositiveInt


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: PositiveInt
    first_name: str
    last_name: str
    phone: str | None = None
    email: str | None = None
    avatar: str | None = None


class ChangeUserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    first_name: str
    last_name: str
