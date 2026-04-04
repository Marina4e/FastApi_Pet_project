from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Book
from app.dependencies import get_db, get_current_user, require_admin

router = APIRouter(prefix="/books")


# 🔹 CREATE — тільки admin
@router.post("/")
def create_book(
        title: str,
        author: str,
        year: int,
        db: Session = Depends(get_db),
        user=Depends(require_admin)
):
    new_book = Book(
        title=title,
        author=author,
        year=year,
        owner_id=user.id
    )

    db.add(new_book)
    db.commit()

    return new_book


# 🔹 GET — всі авторизовані
@router.get("/")
def get_books(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return db.query(Book).all()
