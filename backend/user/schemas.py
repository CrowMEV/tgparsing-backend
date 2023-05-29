from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr, BaseModel
from fastapi_users import schemas


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserLogout(BaseModel):
    status: str


class UserRead(schemas.BaseUser):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    role_id: int

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str
    role_id: int


class UserUpdate(schemas.BaseUserUpdate):
    pass
