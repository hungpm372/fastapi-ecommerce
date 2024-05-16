from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: EmailStr


class UserCreate(UserBase):
    username: str
    password: str


class UserUpdate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    username: str
    email: str
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    address: str | None = None
