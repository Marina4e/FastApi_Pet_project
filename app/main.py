from fastapi import FastAPI

from app.database import Base, engine
from app.auth.routes import router as auth_router
from app.books import router as books_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(books_router)
