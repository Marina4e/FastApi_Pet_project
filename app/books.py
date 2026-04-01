from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Book, User
from app.dependencies import get_db, get_current_user

router = APIRouter(prefix="/books")


@router.post("/")
def create_book(title: str, author: str, year: int,
                db: Session = Depends(get_db),
                user=Depends(get_current_user)):

    db_user = db.query(User).filter(User.email == user["sub"]).first()

    new_book = Book(
        title=title,
        author=author,
        year=year,
        owner_id=db_user.id
    )

    db.add(new_book)
    db.commit()

    return new_book


@router.get("/")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()
