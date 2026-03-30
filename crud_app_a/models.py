from pydantic import BaseModel
from typing import Optional

from sqlalchemy import Column, Integer, String
from database import Base


# 🔹 SQLAlchemy модель (таблиця)
class BookDB(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    year = Column(Integer)


# 🔹 Pydantic (для API)
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int

    class Config:
        from_attributes = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
