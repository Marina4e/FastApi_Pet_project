from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.schemas import BookOut, BookBase
from app.models import Book
from app.dependencies import get_db, get_current_user, require_admin

router = APIRouter(prefix="/books", tags=["Books"])


# 🔹 CREATE — тільки admin
@router.post("/")
def create_book(
        book: BookBase,  # 👈 ВОТ СЮДА
        db: Session = Depends(get_db),
        user=Depends(require_admin)
):
    new_book = Book(
        title=book.title,
        author=book.author,
        year=book.year,
        owner_id=user.id
    )

    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


# 🔹 GET — всі авторизовані
@router.get("/", response_model=list[BookOut])
def get_books(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return db.query(Book).all()


@router.put("/{book_id}")
def update_book(
        book_id: int,
        book: BookBase,  # 👈 ВОТ СЮДА
        db: Session = Depends(get_db),
        user=Depends(require_admin)
):
    book_db = db.query(Book).filter(Book.id == book_id).first()

    if not book_db:
        raise HTTPException(status_code=404, detail="Book not found")

    book_db.title = book.title
    book_db.author = book.author
    book_db.year = book.year

    db.commit()
    db.refresh(book_db)

    return book_db


@router.delete("/{book_id}")
def delete_book(
        book_id: int,
        db: Session = Depends(get_db),
        user=Depends(require_admin),
        current_user=Depends(get_current_user)
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if current_user.role != "admin":
        raise HTTPException(status_code=403)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    print("BOOK ID:", book.id)
    print("OWNER ID:", book.owner_id)

    db.delete(book)
    db.commit()

    return {"msg": "Book deleted"}


@router.get("/{book_id}", response_model=BookOut)
def get_book(
        book_id: int,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)  # 👈 ВОТ СЮДА
):
    book = db.query(Book).filter(Book.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book
