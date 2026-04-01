from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from app.database import SessionLocal
from app.models import User
from app.auth.schemas import UserCreate
from app.auth.jwt import create_access_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 📌 DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📌 get user
def get_user(db, email: str):
    return db.query(User).filter(User.email == email).first()


# ✅ REGISTER (залишається як є)
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user(db, user.email):
        raise HTTPException(status_code=400, detail="User exists")

    new_user = User(
        email=user.email,
        hashed_password=pwd_context.hash(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"msg": "User created"}


# 🔥 LOGIN (ОСЬ ТУТ ГОЛОВНА ЗМІНА)
@router.post("/login")
def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    email = form_data.username  # ⚠️ тут username = email
    password = form_data.password

    db_user = get_user(db, email)

    if not db_user or not pwd_context.verify(password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
