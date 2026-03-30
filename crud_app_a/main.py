from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
from models import BookDB, Book, BookUpdate

app = FastAPI()

# Створення таблиць
Base.metadata.create_all(bind=engine)


# 🔹 Dependency (підключення до БД)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ➕ CREATE
@app.post("/books/", response_model=Book)
def create_book(book: Book, db: Session = Depends(get_db)):
    existing = db.query(BookDB).filter(BookDB.id == book.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Book already exists")

    new_book = BookDB(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


# 📖 READ ALL
@app.get("/books/", response_model=list[Book])
def get_books(db: Session = Depends(get_db)):
    return db.query(BookDB).all()


# 📖 READ ONE
@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


# ✏️ UPDATE
@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book_update.title is not None:
        book.title = book_update.title
    if book_update.author is not None:
        book.author = book_update.author
    if book_update.year is not None:
        book.year = book_update.year

    db.commit()
    db.refresh(book)

    return book


# ❌ DELETE
@app.delete("/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookDB).filter(BookDB.id == book_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted"}
