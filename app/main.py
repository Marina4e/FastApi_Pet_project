from fastapi import FastAPI
from fastapi.responses import FileResponse
from app.auth.routes import router as auth_router
from app.books import router as books_router
from app.articles import router as articles_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(articles_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def get_front():
    return FileResponse("app/frontend.html")
