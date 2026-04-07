from pydantic import BaseModel, EmailStr, ConfigDict


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str | None = "user"


class UserShort(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


class BookBase(BaseModel):
    title: str
    author: str
    year: int


class BookOut(BookBase):
    id: int
    owner: UserShort   # 🔥 ВАЖНО

    model_config = ConfigDict(from_attributes=True)
