from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr, BaseModel, Field
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
    firstname: str = Field(..., min_length=1, regex='^[a-zA-Z]+$')
    lastname: str = Field(..., min_length=1, regex='^[a-zA-Z]+$')
    email: EmailStr
    role_id: int
    password: str = Field(
        ...,
        min_length=8,
        regex=r'([0-9]+\S*[A-Z]+|[A-Z]+\S*[0-9]+)\S*'
              '[!"`\'#%&,:;<>=@{}~\$\(\)\*\+\/\\\?\[\]\^\|]+'
    )


class UserUpdate(schemas.BaseUserUpdate):
    pass
