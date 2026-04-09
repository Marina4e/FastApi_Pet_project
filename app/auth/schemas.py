from pydantic import BaseModel, ConfigDict, EmailStr


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
    owner: UserShort  # 🔥 ВАЖНО

    model_config = ConfigDict(from_attributes=True)


class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleOut(ArticleBase):
    id: int
    owner: UserShort

    model_config = ConfigDict(from_attributes=True)


class UserDetail(BaseModel):
    id: int
    email: str

    articles: list[ArticleOut] = []
    followers: list[UserShort] = []
    following: list[UserShort] = []

    model_config = ConfigDict(from_attributes=True)
