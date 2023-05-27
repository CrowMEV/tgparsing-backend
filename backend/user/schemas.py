from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr
from fastapi_users import schemas


class UserRead(schemas.BaseUser):
    id: int
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(CreateUpdateDictModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str


class UserUpdate(schemas.BaseUserUpdate):
    pass
